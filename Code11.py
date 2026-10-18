
from machine import Pin, SPI
import time

spi = SPI(2, baudrate=100000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23), miso=Pin(19))

cs = Pin(5, Pin.OUT)
cs.value(1)

time.sleep_ms(100)

cs.value(0)
response = spi.read(10, 0xFF)
cs.value(1)

print("SPI response:", response)
