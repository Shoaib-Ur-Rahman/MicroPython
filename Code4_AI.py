
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)
button = Pin(4, Pin.IN, Pin.PULL_UP)

led_state = False
previous = 1

while True:
    current = button.value()

    if current == 0 and previous == 1:
        sleep(0.05)

        if button.value() == 0:
            led_state = not led_state
            led.value(led_state)
            print("On" if led_state else "Off")

    previous = current
    sleep(0.02)
