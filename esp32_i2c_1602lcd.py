import time
from machine import I2C, Pin

class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.backlight = 0x08
        self.i2c.writeto(self.i2c_addr, bytes([0x00]))
        time.sleep_ms(50)
        self._write_init_nibble(0x30)
        time.sleep_ms(5)
        self._write_init_nibble(0x30)
        time.sleep_ms(1)
        self._write_init_nibble(0x30)
        self._write_init_nibble(0x20)
        self.write_cmd(0x28)
        self.write_cmd(0x0C)
        self.write_cmd(0x06)
        self.clear()

    def _write_init_nibble(self, nibble):
        self.i2c.writeto(self.i2c_addr, bytes([nibble | 0x04, nibble]))
        time.sleep_ms(1)

    def write_cmd(self, cmd):
        self._write_nibble(cmd & 0xF0)
        self._write_nibble((cmd << 4) & 0xF0)

    def _write_nibble(self, nibble):
        self.i2c.writeto(self.i2c_addr, bytes([nibble | self.backlight | 0x04, nibble | self.backlight]))

    def write_data(self, data):
        self._write_nibble((data & 0xF0) | 0x01)
        self._write_nibble(((data << 4) & 0xF0) | 0x01)

    def clear(self):
        self.write_cmd(0x01)
        time.sleep_ms(2)
        self.cursor_x = 0
        self.cursor_y = 0

    def move_to(self, cursor_x, cursor_y):
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        addr = cursor_x & 0x3F
        if cursor_y & 1:
            addr += 0x40
        if cursor_y & 2:
            addr += self.num_columns
        self.write_cmd(0x80 | addr)

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.move_to(0, self.cursor_y + 1)
            else:
                self.write_data(ord(char))
