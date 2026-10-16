from machine import Pin
from time import sleep
led=Pin(4, Pin.OUT)
button=Pin(18, Pin.OUT, Pin.PULL_UP)
while True:
    value=button.value()
    if value==0:
        led.on()
    else:
        led.off()
    sleep(1)