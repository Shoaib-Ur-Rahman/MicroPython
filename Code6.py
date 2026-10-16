from machine import Pin, ADC, PWM
from time import sleep
led = Pin(4, Pin.OUT)
adc = ADC(Pin(34), atten=ADC.ATTN_11DB)
adc.block().init(bits=12)
reading = adc.read_u16()
# ADC potentiometer setup
adc = ADC(Pin(34))

# UPDATED: replaces deprecated atten() and width()
adc.init(atten=ADC.ATTN_11DB, bits=12)

while True:
    # UPDATED: replaces deprecated read()
    reading = adc.read_u16()
    print("ADC reading:", reading)

    # NEW: use the ADC reading to control LED brightness
    brightness = reading
    led.value(brightness)

    sleep(0.5)