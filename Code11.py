from machine import Pin, SPI
spi = SPI(2, baudrate=1000000, polarity=0, phase=0, sck=Pin())