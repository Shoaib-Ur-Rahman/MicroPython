from machine import Pin, I2C
from time import sleep

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=100000
)

print(i2c.scan())