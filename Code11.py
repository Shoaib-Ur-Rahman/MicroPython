from machine import Pin

miso = Pin(19, Pin.IN, Pin.PULL_UP)
print("MISO connected:", miso.value())