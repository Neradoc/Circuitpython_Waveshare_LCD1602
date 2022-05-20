# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) Waveshare
# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
#
# SPDX-License-Identifier: MIT
#
# In order to keep basic compatibility with the orifinal library, ignore "bad" names.
# pylint: disable=invalid-name
"""
`waveshare_lcd1602`
================================================================================

Drive for Waveshare's I2C character display LCD1602.
A port of Waveshare's RGB1602 Micropython library.

* Author(s): Neradoc

Implementation Notes
--------------------

**Hardware:**

* `Waveshare LCD1602 RGB Module <https://www.waveshare.com/wiki/LCD1602_RGB_Module>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time
from adafruit_bus_device.i2c_device import I2CDevice

try:
    from typing import Union
    import busio
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/Neradoc/Circuitpython_Waveshare_LCD1602.git"

# Device I2C Arress
LCD_ADDRESS = 0x7C >> 1
RGB_ADDRESS = 0xC0 >> 1

# color define

REG_RED = 0x04
REG_GREEN = 0x03
REG_BLUE = 0x02
REG_MODE1 = 0x00
REG_MODE2 = 0x01
REG_OUTPUT = 0x08
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5X8DOTS = 0x00


class LCD1602:
    """
    Setup a new RGB LCD1602 display

    :param busio.I2C i2c: I2C bus object to use.
    :param int columns: The number of columns on the display.
    :param int rows: The number of rows on the display.
    """

    def __init__(self, i2c: busio.I2C, columns: int, rows: int):
        self.lcd_device = I2CDevice(i2c, LCD_ADDRESS)
        self.rgb_device = I2CDevice(i2c, RGB_ADDRESS)
        self._row = rows
        self._col = columns

        self._showfunction = LCD_4BITMODE | LCD_1LINE | LCD_5X8DOTS
        self.begin(self._row, self._col)

    def command(self, cmd: int):
        """
        Send a command.

        :param int cmd: The command code.
        """
        with self.lcd_device:
            self.lcd_device.write(bytes([0x80]) + chr(cmd))

    def write(self, data: int):
        """
        Write a data byte.

        :param int data: The data byte to write.
        """
        with self.lcd_device:
            self.lcd_device.write(bytes([0x40]) + chr(data))

    def setReg(self, reg, data):
        """
        Set the value of a register.

        :param int reg: The register to write to.
        :param int data: The data byte to write.
        """
        with self.rgb_device:
            self.rgb_device.write(bytes([reg]) + chr(data))

    def setRGB(self, r, g, b):
        """
        Set the color of the RGB backlight.

        :param int r: Red byte.
        :param int g: Green byte.
        :param int b: Blue byte.
        """
        self.setReg(REG_RED, r)
        self.setReg(REG_GREEN, g)
        self.setReg(REG_BLUE, b)

    def setCursor(self, col, row):
        """
        Place the cursor on the display.

        :param int col: The column.
        :param int row: The row.
        """
        if row == 0:
            col |= 0x80
        else:
            col |= 0xC0
        with self.lcd_device:
            self.lcd_device.write(bytearray([0x80, col]))

    def clear(self):
        """Clear the display."""
        self.command(LCD_CLEARDISPLAY)
        time.sleep(0.002)

    def printout(self, arg: Union[str, int]):
        """
        Print a string to the display. Ints are converted to strings.

        :param str|int arg: The string or int to printout.
        """
        if isinstance(arg, int):
            arg = str(arg)

        for x in bytearray(arg, "utf-8"):
            self.write(x)

    def display(self):
        """Turn on the display."""
        self._showcontrol |= LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._showcontrol)

    def begin(self, columns: int, rows: int):  # pylint: disable=unused-argument
        """
        Initial configuration, called from init.

        :param int columns: The number of columns on the display.
        :param int rows: The number of rows on the display.
        """
        if rows > 1:
            self._showfunction |= LCD_2LINE

        self._numlines = rows
        self._currline = 0

        time.sleep(0.05)

        # Send function set command sequence
        self.command(LCD_FUNCTIONSET | self._showfunction)
        # delayMicroseconds(4500);  # wait more than 4.1ms
        time.sleep(0.005)
        # second try
        self.command(LCD_FUNCTIONSET | self._showfunction)
        # delayMicroseconds(150);
        time.sleep(0.005)
        # third go
        self.command(LCD_FUNCTIONSET | self._showfunction)
        # finally, set # lines, font size, etc.
        self.command(LCD_FUNCTIONSET | self._showfunction)
        # turn the display on with no cursor or blinking default
        self._showcontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display()
        # clear it off
        self.clear()
        # Initialize to default text direction (for romance languages)
        self._showmode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        # set the entry mode
        self.command(LCD_ENTRYMODESET | self._showmode)
        # backlight init
        self.setReg(REG_MODE1, 0)
        # set LEDs controllable by both PWM and GRPPWM registers
        self.setReg(REG_OUTPUT, 0xFF)
        # set MODE2 values
        # 0010 0000 -> 0x20  (DMBLNK to 1, ie blinky mode)
        self.setReg(REG_MODE2, 0x20)
        self.setColorWhite()

    def setColorWhite(self):
        """Set the color of the RGB backlight to white."""
        self.setRGB(255, 255, 255)
