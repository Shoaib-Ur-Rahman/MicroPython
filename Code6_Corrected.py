from machine import Pin, ADC, PWM
from time import sleep

led = PWM(Pin(4), freq=1000)

# ADC potentiometer setup
adc = ADC(Pin(34))
adc.init(atten=ADC.ATTN_11DB)

while True:
    reading = adc.read_u16()
    print("ADC reading:", reading)

    led.duty_u16(reading)

    sleep(0.5)