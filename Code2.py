from machine import Pin, PWM
from time import sleep

led = PWM(Pin(18), freq=1000)
led.duty_u16(0)

while True:
    led.duty_u16(0)
    sleep(0.1)
    led.duty_u16(65535)
    sleep(0.1)