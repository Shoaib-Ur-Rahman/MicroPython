from machine import Pin, SPI
import sdcard
import os
spi=SPI(2, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
sd=sdcard.SDCard(spi, Pin(5))
class SDPartition:
    def _init_(self, sd, start_sector):
        self.sd
        self.start_sector(3805184)
        self.size(2048)
        