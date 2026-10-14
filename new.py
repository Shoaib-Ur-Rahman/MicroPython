from machine import Pin
from time import sleep
print("ESP32 is running!")
while True:
    print(Pin(4, Pin.IN, Pin.PULL_UP).value(), end="")
    sleep(0.1)