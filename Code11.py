from machine import Pin
import time

cs = Pin(5, Pin.OUT, value=1)
miso = Pin(19, Pin.IN)

time.sleep_ms(100)

print("MISO with CS HIGH:", miso.value())

cs.value(0)
time.sleep_ms(10)
print("MISO with CS LOW:", miso.value())

cs.value(1)