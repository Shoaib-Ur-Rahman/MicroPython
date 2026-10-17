from machine import Pin, I2C
from lcd_i2c import LCD
import time

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
lcd = LCD(addr=0x27, cols=16, rows=2, i2c=i2c)

lcd.begin()
lcd.backlight()
lcd.clear()
lcd.print("Hello, World!")