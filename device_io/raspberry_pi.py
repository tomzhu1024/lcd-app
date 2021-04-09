import signal
import sys
import time

import numpy as np
from PIL import Image

from ._prototype import Prototype

try:
    import RPi.GPIO as GPIO
    from gpiozero import Button
    import spidev
except ImportError as ex:
    raise ex

# constants
# pin for screen
screen_rst = 27
screen_dc = 25
screen_bl = 24
# spi bus no. and device no.
spi_bus = 0
spi_device = 0
# pin for buttons
button_up_pin = 6
button_down_pin = 19
button_left_pin = 5
button_right_pin = 26
button_center_pin = 13
button_1_pin = 21
button_2_pin = 20
button_3_pin = 16
# duration for debouncing
bounce_time = 400


class ST7789:
    """Class for ST7789 240*240 1.3inch OLED displays."""

    def __init__(self, spi, rst, dc, bl):
        self.width = 240
        self.height = 240
        # Initialize DC RST pin
        self._dc = dc
        self._rst = rst
        self._bl = bl
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._dc, GPIO.OUT)
        GPIO.setup(self._rst, GPIO.OUT)
        GPIO.setup(self._bl, GPIO.OUT)
        GPIO.output(self._bl, GPIO.HIGH)
        # Initialize SPI
        self._spi = spi
        self._spi.max_speed_hz = 40000000

    def _command(self, cmd):
        GPIO.output(self._dc, GPIO.LOW)
        self._spi.writebytes([cmd])

    def _data(self, val):
        GPIO.output(self._dc, GPIO.HIGH)
        self._spi.writebytes([val])

    def init(self):
        """Initialize display."""
        self.reset()

        self._command(0x11)
        time.sleep(1.2)
        self._command(0x36)
        self._data(0X70)

        self._command(0x3A)
        self._data(0x05)

        self._command(0xB2)
        self._data(0x0C)
        self._data(0x0C)
        self._data(0x00)
        self._data(0x33)
        self._data(0x33)

        self._command(0xB7)
        self._data(0x35)

        self._command(0xBB)
        self._data(0x37)

        self._command(0xC0)
        self._data(0x2C)

        self._command(0xC2)
        self._data(0x01)

        self._command(0xC3)
        self._data(0x12)

        self._command(0xC4)
        self._data(0x20)

        self._command(0xC6)
        self._data(0x0F)

        self._command(0xD0)
        self._data(0xA4)
        self._data(0xA1)

        self._command(0xE0)
        self._data(0xD0)
        self._data(0x04)
        self._data(0x0D)
        self._data(0x11)
        self._data(0x13)
        self._data(0x2B)
        self._data(0x3F)
        self._data(0x54)
        self._data(0x4C)
        self._data(0x18)
        self._data(0x0D)
        self._data(0x0B)
        self._data(0x1F)
        self._data(0x23)

        self._command(0xE1)
        self._data(0xD0)
        self._data(0x04)
        self._data(0x0C)
        self._data(0x11)
        self._data(0x13)
        self._data(0x2C)
        self._data(0x3F)
        self._data(0x44)
        self._data(0x51)
        self._data(0x2F)
        self._data(0x1F)
        self._data(0x1F)
        self._data(0x20)
        self._data(0x23)

        self._command(0x21)

        self._command(0x29)

    def reset(self):
        """Reset the display."""
        GPIO.output(self._rst, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self._rst, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self._rst, GPIO.HIGH)
        time.sleep(0.01)

    def _set_windows(self, x_start, y_start, x_end, y_end):
        # Set the X coordinates
        self._command(0x2A)
        self._data(0x00)  # Set the horizontal starting point to the high octet
        self._data(x_start & 0xff)  # Set the horizontal starting point to the low octet
        self._data(0x00)  # Set the horizontal end to the high octet
        self._data((x_end - 1) & 0xff)  # Set the horizontal end to the low octet
        # Set the Y coordinates
        self._command(0x2B)
        self._data(0x00)
        self._data((y_start & 0xff))
        self._data(0x00)
        self._data((y_end - 1) & 0xff)

        self._command(0x2C)

    def show_image(self, image):
        """Set buffer to value of Python Imaging Library image."""
        # Write display buffer to physical display
        im_width, im_height = image.size
        if im_width != self.width or im_height != self.height:
            raise ValueError('Image must be same dimensions as display ({0}x{1}).'.format(self.width, self.height))
        img = np.asarray(image)
        pix = np.zeros((self.width, self.height, 2), dtype=np.uint8)
        pix[..., [0]] = np.add(np.bitwise_and(img[..., [0]], 0xF8), np.right_shift(img[..., [1]], 5))
        pix[..., [1]] = np.add(np.bitwise_and(np.left_shift(img[..., [1]], 3), 0xE0), np.right_shift(img[..., [2]], 3))
        pix = pix.flatten().tolist()
        self._set_windows(0, 0, self.width, self.height)
        GPIO.output(self._dc, GPIO.HIGH)
        for i in range(0, len(pix), 4096):
            self._spi.writebytes(pix[i:i + 4096])

    def clear(self):
        """Clear contents of image buffer."""
        _buffer = [0x00] * (self.width * self.height * 2)
        self._set_windows(0, 0, self.width, self.height)
        GPIO.output(self._dc, GPIO.HIGH)
        for i in range(0, len(_buffer), 4096):
            self._spi.writebytes(_buffer[i:i + 4096])


class RaspberryPi(Prototype):
    """Class for Raspberry Pi device inputs and outputs."""

    def __init__(self):
        super().__init__()
        # initiate display
        self.display = ST7789(spidev.SpiDev(spi_bus, spi_device), screen_rst, screen_dc, screen_bl)
        self.display.init()
        self.display.clear()  # clear any remaining content
        # initiate buttons
        self._button_up = Button(button_up_pin)
        self._button_down = Button(button_down_pin)
        self._button_left = Button(button_left_pin)
        self._button_right = Button(button_right_pin)
        self._button_center = Button(button_center_pin)
        self._button_1 = Button(button_1_pin)
        self._button_2 = Button(button_2_pin)
        self._button_3 = Button(button_3_pin)
        # listeners for button pressed events
        self._button_up.when_pressed = self._on_button_up_pressed
        self._button_down.when_pressed = self._on_button_down_pressed
        self._button_left.when_pressed = self._on_button_left_pressed
        self._button_right.when_pressed = self._on_button_right_pressed
        self._button_center.when_pressed = self._on_button_center_pressed
        self._button_1.when_pressed = self._on_button_1_pressed
        self._button_2.when_pressed = self._on_button_2_pressed
        self._button_3.when_pressed = self._on_button_3_pressed
        # listeners for button released events
        self._button_up.when_released = self._on_button_up_released
        self._button_down.when_released = self._on_button_down_released
        self._button_left.when_released = self._on_button_left_released
        self._button_right.when_released = self._on_button_right_released
        self._button_center.when_released = self._on_button_center_released
        self._button_1.when_released = self._on_button_1_released
        self._button_2.when_released = self._on_button_2_released
        self._button_3.when_released = self._on_button_3_released

        # system signal handler
        def signal_handler(*_):
            self.display.reset()
            sys.exit(0)

        # listen to system signals
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def update_display(self, image: Image):
        self.display.show_image(image)


__all__ = ['RaspberryPi']
