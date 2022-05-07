import RGB1602
import time
import math
import board
import busio

colorR = 64
colorG = 128
colorB = 64

"""Default I2C ports on boards that have one"""
i2c = board.I2C()
# i2c = board.STEMMA_I2C()
"""Default pins used by the original code for pico"""
# i2c = busio.I2C(board.GP5, board.GP4)

lcd = RGB1602.RGB1602(i2c, 16, 2)

t = 0
while True:
    r = int((abs(math.sin(3.14 * t / 180))) * 255)
    g = int((abs(math.sin(3.14 * (t + 60) / 180))) * 255)
    b = int((abs(math.sin(3.14 * (t + 120) / 180))) * 255)
    t = t + 3

    lcd.setRGB(r, g, b)

    # set the cursor to column 0, line 1
    lcd.setCursor(0, 0)
    lcd.printout("Waveshare")
    lcd.setCursor(0, 1)
    lcd.printout(f"Loop {t//3}")
    time.sleep(0.3)
