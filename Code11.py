from machine import Pin

miso = Pin(19, Pin.IN)
print("MISO disconnected:", miso.value())