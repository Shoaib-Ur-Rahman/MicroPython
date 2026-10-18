from machine import Pin, SPI
import sdcard

spi = SPI(2, baudrate=100000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23), miso=Pin(19))

print("Starting SD initialization...")
sd = sdcard.SDCard(spi, Pin(5))
print("SD card initialized!")