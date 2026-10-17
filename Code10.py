from machine import Pin, I2C
i2c = I2C(0, sda=Pin(21), scl)