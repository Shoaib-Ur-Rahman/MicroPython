from machine import Pin, SPI
import sdcard
import os

spi = SPI(
    2,
    baudrate=100000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(23),
    miso=Pin(19)
)

sd = sdcard.SDCard(spi, Pin(5))
print("Card initialized:", sd.sectors, "sectors")
class SDPartition:
    def __init__(self, card, start, size):
        self.card = card
        self.start = start
        self.size = size

    def readblocks(self, block_num, buf):
        return self.card.readblocks(self.start + block_num, buf)

    def writeblocks(self, block_num, buf):
        return self.card.writeblocks(self.start + block_num, buf)

    def ioctl(self, op, arg):
        if op == 4:
            return self.size
        if op == 5:
            return 512
        return self.card.ioctl(op, arg)

partition = SDPartition(sd, 2048, 3803103)
vfs = os.VfsFat(partition)
os.mount(vfs, "/sd")
with open("/sd/test.txt", "w") as f:
    f.write("Hello from ESP32!")

with open("/sd/test.txt", "r") as f:
    print("File contents:", f.read())

print("SD contents:", os.listdir("/sd"))
print("Mounted!")
print("SD contents:", os.listdir("/sd"))