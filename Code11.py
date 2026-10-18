
from machine import Pin, SPI
import time

spi = SPI(2, baudrate=100000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23), miso=Pin(19))

cs = Pin(5, Pin.OUT, value=1)

def command(cmd, arg):
    cs.value(1)
    spi.write(b"\xff" * 10)
    cs.value(0)

    packet = bytearray([
        0x40 | cmd,
        (arg >> 24) & 0xff,
        (arg >> 16) & 0xff,
        (arg >> 8) & 0xff,
        arg & 0xff,
        0x87 if cmd == 0 else 0x01
    ])
    spi.write(packet)

    response = 0xff
    for _ in range(10):
        response = spi.read(1, 0xff)[0]
        if not (response & 0x80):
            break

    cs.value(1)
    spi.write(b"\xff")
    return response

print("CMD0 response:", hex(command(0, 0)))
print("CMD8 response:", hex(command(8, 0x1aa)))
