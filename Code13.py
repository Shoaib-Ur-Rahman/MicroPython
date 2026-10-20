from machine import Pin,SPI
import sdcard
import os
spi=SPI(2, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), miso=Pin(19), mosi=Pin(23))
sd=sdcard.SDCard(spi, Pin(5))
os.mount(sd, "/sd")
print("The contents Of The SD", os.listdir())
with open("/sd/log.txt", "w") as f:
    f.write("ESP32 Started Logging")
with open("/sd/log.txt", "r") as f:
    print("The current data:", f.read())