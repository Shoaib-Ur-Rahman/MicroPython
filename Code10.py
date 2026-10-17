from machine import Pin, I2C
import time


class LCD:
	"""Basic HD44780 driver for a PCF8574 I2C LCD backpack."""

	def __init__(self, addr, cols, rows, i2c):
		self.addr = addr
		self.cols = cols
		self.rows = rows
		self.i2c = i2c
		self._backlight = 0

	def _write_nibble(self, value, rs=0):
		data = (value & 0xF0) | self._backlight | rs
		self.i2c.writeto(self.addr, bytes((data | 0x04,)))
		self.i2c.writeto(self.addr, bytes((data & 0xFB,)))

	def _write(self, value, rs=0):
		self._write_nibble(value & 0xF0, rs)
		self._write_nibble((value << 4) & 0xF0, rs)

	def begin(self):
		time.sleep_ms(50)
		for _ in range(3):
			self._write_nibble(0x30)
			time.sleep_ms(5)
		self._write_nibble(0x20)
		self._write(0x28)  # 4-bit interface, two-line display
		self._write(0x0C)  # Display on, cursor off
		self.clear()
		self._write(0x06)  # Move cursor right after each character

	def backlight(self):
		self._backlight = 0x08
		self.i2c.writeto(self.addr, bytes((self._backlight,)))

	def clear(self):
		self._write(0x01)
		time.sleep_ms(2)

	def print(self, text):
		for char in str(text):
			self._write(ord(char), 1)

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
lcd = LCD(addr=0x27, cols=16, rows=2, i2c=i2c)

lcd.begin()
lcd.backlight()
lcd.clear()
lcd.print("Hello, World!")