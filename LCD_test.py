import time
from machine import Pin, I2C
from esp32_i2c_1602lcd import I2cLcd # Ensure you have this library uploaded

# --- Configuration ---
# ESP32 Onboard LED is typically on GPIO 2
LED_PIN = 2 

# Common ESP32 I2C Pins: SDA = GPIO 21, SCL = GPIO 22
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22

# Common LCD I2C addresses are 0x27 or 0x3F
LCD_I2C_ADDR = 0x27 
LCD_ROWS = 2
LCD_COLS = 16

# --- Initialization ---
# Initialize LED
led = Pin(LED_PIN, Pin.OUT)

# Initialize I2C and LCD
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)
lcd = I2cLcd(i2c, LCD_I2C_ADDR, LCD_ROWS, LCD_COLS)

# --- Test Script Run ---
print("Starting LCD and Blinky test...")
lcd.clear()
lcd.putstr("ESP32 Test\nBlinky Active!")

blink_count = 0

try:
    while True:
        # Toggle LED state
        led.value(not led.value())
        
        # Update LCD screen to show it's alive and counting
        lcd.move_to(0, 1) # Move to second row
        lcd.putstr("Blinks: {}   ".format(blink_count))
        
        if led.value():
            blink_count += 1
            
        time.sleep(0.5) # Blink every 500ms

except KeyboardInterrupt:
    # Cleanup on stop
    led.off()
    lcd.clear()
    lcd.putstr("Test Stopped")
    print("Test stopped by user.")
