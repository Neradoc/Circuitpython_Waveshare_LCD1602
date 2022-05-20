Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-waveshare-lcd1602/badge/?version=latest
    :target: https://circuitpython-waveshare-lcd1602.readthedocs.io/
    :alt: Documentation Status



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/Neradoc/CircuitPython_Waveshare_LCD1602/workflows/Build%20CI/badge.svg
    :target: https://github.com/Neradoc/CircuitPython_Waveshare_LCD1602/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Drive for Waveshare's I2C character display LCD1602


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-waveshare-lcd1602/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-waveshare-lcd1602

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-waveshare-lcd1602

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install circuitpython-waveshare-lcd1602



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install waveshare_lcd1602

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. python:
    import waveshare_lcd1602
    import time
    import math
    import board
    import busio

    from rainbowio import colorwheel

    """Default I2C ports on boards that have one"""
    i2c = board.I2C()
    # i2c = board.STEMMA_I2C()
    """Default pins used by the original code for pico"""
    # i2c = busio.I2C(board.GP5, board.GP4)

    lcd = waveshare_lcd1602.LCD1602(i2c, 16, 2)
    lcd.setRGB(255, 255, 0)
    lcd.setCursor(0, 0)
    lcd.printout("Waveshare")
    lcd.setCursor(0, 1)
    lcd.printout(f"Hellow World !")

    while True:
        color = colorwheel(time.monotonic()*16)
        lcd.setRGB(color >> 16, (color >> 8) % 0x100, color % 0x100)
        time.sleep(1)


Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-waveshare-lcd1602.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/Neradoc/Circuitpython_Waveshare_LCD1602/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
