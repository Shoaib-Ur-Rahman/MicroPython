
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)

while True:
    led.on()
    print("LED ON")
    sleep(0.1)

    led.off()
    print("LED OFF")
    sleep(0.2)
