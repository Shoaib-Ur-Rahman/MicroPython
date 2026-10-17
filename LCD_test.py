import time
from machine import Pin, I2C

# ==========================================
# 1. EMBEDDED LCD DRIVER (No library files needed)
# ==========================================
class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.backlight = 0x08
        try:
            self.i2c.writeto(self.i2c_addr, bytes([0x00]))
        except OSError:
            print(f"Error: Could not find I2C device at address {hex(i2c_addr)}")
        time.sleep_ms(50)
        self._write_init_nibble(0x30)
        time.sleep_ms(5)
        self._write_init_nibble(0x30)
        time.sleep_ms(1)
        self._write_init_nibble(0x30)
        self._write_init_nibble(0x20)
        self.write_cmd(0x28)
        self.write_cmd(0x0C)
        self.write_cmd(0x06)
        self.clear()

    def _write_init_nibble(self, nibble):
        self.i2c.writeto(self.i2c_addr, bytes([nibble | 0x04, nibble]))
        time.sleep_ms(1)

    def write_cmd(self, cmd):
        self._write_nibble(cmd & 0xF0)
        self._write_nibble((cmd << 4) & 0xF0)

    def _write_nibble(self, nibble):
        self.i2c.writeto(self.i2c_addr, bytes([nibble | self.backlight | 0x04, nibble | self.backlight]))

    def write_data(self, data):
        self._write_nibble((data & 0xF0) | 0x01)
        self._write_nibble(((data << 4) & 0xF0) | 0x01)

    def clear(self):
        self.write_cmd(0x01)
        time.sleep_ms(2)
        self.cursor_x = 0
        self.cursor_y = 0

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40
        if cursor_y & 2:
            addr += self.num_columns
        self.write_cmd(0x80 | addr)

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.move_to(0, self.cursor_y + 1)
            else:
                self.write_data(ord(char))

# ==========================================
# 2. HARDWARE CONFIGURATION
# ==========================================
LED_PIN = 2          # Onboard LED (GPIO 2)
I2C_SDA_PIN = 21     # Default ESP32 SDA
I2C_SCL_PIN = 22     # Default ESP32 SCL

LCD_I2C_ADDR = 0x27  # Change to 0x3F if your screen stays blank
LCD_ROWS = 2
LCD_COLS = 16

# ==========================================
# 3. INITIALIZATION & MAIN LOOP
# ==========================================
led = Pin(LED_PIN, Pin.OUT)
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)

# Scan to see what I2C devices are actually connected
print("Scanning I2C bus...")
devices = i2c.scan()
print("Found I2C addresses:", [hex(d) for d in devices])

lcd = I2cLcd(i2c, LCD_I2C_ADDR, LCD_ROWS, LCD_COLS)

print("Starting combined test...")
lcd.clear()
lcd.putstr("ESP32 Test\nBlinky Running!")

blink_count = 0

try:
    while True:
        led.value(not led.value()) # Toggle LED
        
        lcd.move_to(0, 1) # Move to second row
        lcd.putstr("Count: {}     ".format(blink_count))
        
        if led.value():
            blink_count += 1
            
        time.sleep(0.5)

except KeyboardInterrupt:
    led.off()
    lcd.clear()
    lcd.putstr("Test Stopped")
    print("Stopped by user.")
