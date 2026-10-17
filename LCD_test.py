import time
import random
from machine import Pin, I2C

# ==========================================
# 1. EMBEDDED LCD DRIVER
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
            print(f"Error: Device missing at {hex(i2c_addr)}")
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
# 2. CONFIGURATION & SETUP
# ==========================================
LED_PIN = 2
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22
LCD_I2C_ADDR = 0x27
LCD_ROWS = 2
LCD_COLS = 16

led = Pin(LED_PIN, Pin.OUT)
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)
lcd = I2cLcd(i2c, LCD_I2C_ADDR, LCD_ROWS, LCD_COLS)

# Pool of characters to pull chaos from
CHAR_POOL = "$@#%&*+-/;<=>?[]^_{|}~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Generate random paths of symbols
line1_stream = "".join(random.choice(CHAR_POOL) for _ in range(60))
line2_stream = "".join(random.choice(CHAR_POOL) for _ in range(60))

# Loop extensions
line1_stream += line1_stream[:LCD_COLS]
line2_stream += line2_stream[:LCD_COLS]

frame = 0
print("Running relaxed chaos slider...")

# ==========================================
# 3. MAIN LOOP
# ==========================================
try:
    while True:
        # Toggle LED
        led.value(not led.value())

        # Slide Line 1 Left
        start_idx_1 = frame % (len(line1_stream) - LCD_COLS)
        chunk_1 = line1_stream[start_idx_1 : start_idx_1 + LCD_COLS]
        lcd.move_to(0, 0)
        lcd.putstr(chunk_1)

        # Slide Line 2 Right (Opposite direction)
        start_idx_2 = (len(line2_stream) - LCD_COLS - frame) % (len(line2_stream) - LCD_COLS)
        chunk_2 = line2_stream[start_idx_2 : start_idx_2 + LCD_COLS]
        lcd.move_to(0, 1)
        lcd.putstr(chunk_2)

        frame += 1
        
        # Slower sleep time to let pixels cool down and keep readability sharp
        time.sleep(0.60) 

except KeyboardInterrupt:
    led.off()
    lcd.clear()
    lcd.putstr("Chaos Paused")
