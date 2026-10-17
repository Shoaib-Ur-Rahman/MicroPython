from machine import Pin, PWM
import time

buzzer = PWM(Pin(25), freq=2000, duty_u16=32768)
time.sleep(2)

buzzer.duty_u16(0)
buzzer.deinit()