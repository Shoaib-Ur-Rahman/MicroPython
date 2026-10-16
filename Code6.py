from machine import Pin, ADC, PWM
from time import sleep
led = Pin(4, Pin.OUT)
# ADC potentiometer setup
adc = ADC(Pin(34))
adc.init(atten=ADC.ATTN_11DB)

while True:
    # UPDATED: replaces deprecated read()
    reading = adc.read_u16()
    print("ADC reading:", reading)

    # NEW: use the ADC reading to control LED brightness
    brightness = reading
    led.value(brightness)

    sleep(0.5)