from machine import Pin, PWM

led = PWM(Pin(4), freq=1000)
print(dir(led))