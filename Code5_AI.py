
from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)
button = Pin(4, Pin.IN, Pin.PULL_UP)

led_state = False
previous = 1

while True:
    current = button.value()

    if current != previous:
        sleep(0.05)
        current = button.value()

        if current != previous:
            previous = current

            if current == 0:
                led_state = not led_state
                led.value(led_state)
                print("On" if led_state else "Off")

    sleep(0.01)
