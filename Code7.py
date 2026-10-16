from machine import Pin, PWM, ADC
from time import sleep

adc=ADC(Pin(34))
adc.init(atten=ADC.ATTN_11DB)
led=PWM(Pin(4), freq=1000)
while True:
    reading=adc.read_u16()
    led.duty_u16(reading)
    print("ADC reading: ", reading)
    sleep(0.5)