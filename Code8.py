from machine import Pin, ADC,PWM
from time import sleep

sensor = ADC(Pin(34))
sensor.init(atten=ADC.ATTN_11DB)
led=PWM(Pin(4),freq=1000)

while True:
    reading=sensor.read_u16()
    print("ADC Reading", sensor.read_u16())
    led.duty_u16(reading)
    sleep(0.5)