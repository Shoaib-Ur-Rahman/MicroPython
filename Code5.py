from machine import Pin
from time import sleep
led = Pin(18, Pin.OUT)
button = Pin(4, Pin.IN, Pin.PULL_UP)
previous = 1
led_state=0
while True:
    current=button.value()
    if current == 0 and previous == 1:
        sleep(0.5)
        if button == 0:
            led_state= not led_state
            led.value(led_state)
    previous=current
    sleep(0.09)