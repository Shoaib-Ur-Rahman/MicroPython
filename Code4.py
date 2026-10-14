from machine import Pin, PWM
from time import sleep
led = PWM(Pin(18), freq=1000)
while True:
    led.duty_u16(65535)
    sleep(1)
    led.duty_u16(32767)
    sleep(1)