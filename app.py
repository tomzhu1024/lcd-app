import os
import re
import signal
import socket
import sys
import time

import RPi.GPIO as GPIO
import spidev as SPI
from PIL import Image

from device_io import raspberry_pi
import page_switcher
from shared_utils import ProtoDeviceCapabilities

# GPIO definition
KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16

RST = 27
DC = 25
BL = 24
bus = 0
device = 0

# hardware
BOUNCE_TIME = 250
BATTERY_HISTORY = 10

# refresh rate
TICK_INTERVAL = 0.1

disp = raspberry_pi.ST7789(SPI.SpiDev(bus, device), RST, DC, BL)
disp.init()
disp.show_image(Image.new('RGB', (240, 240), (0, 0, 0)), 0, 0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def on_key_up(channel):
    page_switcher.on_key_up()


def on_key_right(channel):
    page_switcher.on_key_right()


def on_key_down(channel):
    page_switcher.on_key_down()


def on_key_left(channel):
    page_switcher.on_key_left()


def on_key_press(channel):
    page_switcher.on_key_press()


def on_key_1(channel):
    page_switcher.on_key_1()


def on_key_2(channel):
    page_switcher.on_key_2()


def on_key_3(channel):
    page_switcher.on_key_3()


GPIO.add_event_detect(KEY_UP_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_up)
GPIO.add_event_detect(KEY_DOWN_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_down)
GPIO.add_event_detect(KEY_LEFT_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_left)
GPIO.add_event_detect(KEY_RIGHT_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_right)
GPIO.add_event_detect(KEY_PRESS_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_press)
GPIO.add_event_detect(KEY1_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_1)
GPIO.add_event_detect(KEY2_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_2)
GPIO.add_event_detect(KEY3_PIN, GPIO.FALLING, bouncetime=BOUNCE_TIME, callback=on_key_3)


class RaspberryPiCapabilities(ProtoDeviceCapabilities):
    def _query_sock(self, query):
        try:
            self._conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._conn.connect('/tmp/pisugar-server.sock')
            self._conn.send(query.encode())
            rtn = ''
            while True:
                char = self._conn.recv(1).decode()
                if char != '\n':
                    rtn += char
                else:
                    break
            self._conn.close()
            return rtn
        except:
            return ''

    def update_screen(self, image):
        disp.show_image(image, 0, 0)

    def get_ip_addr(self):
        p_rtn = ''.join(os.popen('ifconfig').readlines())
        ip_addr = re.findall(r'.*wlan0:.*?inet(.*?)netmask.*', p_rtn, re.S)
        ip_addr = ip_addr[0].strip() if len(ip_addr) > 0 else ''
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_addr) is not None:
            return ip_addr
        else:
            return '---.---.---.---'

    def socket_command(self, command):
        s_rtn = self._query_sock(command)
        if re.match(r'.*?: .*', s_rtn) is not None:
            i_rtn = re.findall(r'.*?: (.*)', s_rtn)[0].strip()
        else:
            i_rtn = None
        return i_rtn


raspberry_pi_capabilities = RaspberryPiCapabilities()


def signal_handler(signal, frame):
    disp.reset()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

while True:
    time.sleep(time.time() % TICK_INTERVAL)
    page_switcher.on_tick(raspberry_pi_capabilities)
