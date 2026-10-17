import time
from machine import Pin, I2C

# Reset I2C on standard pins
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)

while True:
    print("Scanning for LCD...")
    devices = i2c.scan()
    print("Found addresses:", [hex(d) for d in devices])
    time.sleep(2)
