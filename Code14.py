from machine import Pin, SPI
import os, sdcard
spi=SPI(2, baudrate=10000000, polarity=0, phase=0, mosi=Pin(23), miso=Pin(19), sck=Pin(18))
sd=sdcard.SDCard(spi, Pin(5))
os.mount(sd, "/sd")
print("Files on sd", os.listdir("/sd"))
with open("/sd/log.txt", "a") as f:
    f.write("\nThis is the relog that the ESP32 is dying of rewriting the same thing")
with open("/sd/log.txt", "r") as f:
    print(f.read())