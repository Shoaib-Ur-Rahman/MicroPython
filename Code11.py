from machine import Pin, SPI
import sdcard
import os
spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
sd = sdcard.SDCard(spi, Pin(5))
os.mount(sd, "/sd")
print("SD card Mounted")
print(os.listdir("/sd"))