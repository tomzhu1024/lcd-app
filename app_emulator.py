import sys
import threading
import time

from PIL import Image, ImageQt
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QDesktopWidget

import page_switcher
from shared_utils import ProtoDeviceCapabilities

# window style
window_width = 700
window_height = 280
left_keys_size = 40
left_keys_sprawl = 60
right_keys_x_size = 80
right_keys_y_size = 35
right_keys_sprawl = 40
left_keys_x_pos = (window_width / 2 - 120) / 2
SC_XPOS = window_width / 2
RK_XPOS = window_width - left_keys_x_pos

# refresh rate
TICK_INTERVAL = 0.1


class EmulatorWindow(QWidget):
    def __init__(self):
        super().__init__()

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(QRect(screen.width() / 2 - window_width / 2,
                               screen.height() / 2 - window_height / 2,
                               window_width, window_height))
        self.setWindowTitle('LCD APP Emulator')
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.btn_up = QPushButton(self)
        self.btn_up.setText('U')
        self.btn_up.setGeometry(QRect(left_keys_x_pos - left_keys_size / 2,
                                      window_height / 2 - left_keys_sprawl - left_keys_size / 2,
                                      left_keys_size, left_keys_size))
        self.btn_right = QPushButton(self)
        self.btn_right.setText('R')
        self.btn_right.setGeometry(QRect(left_keys_x_pos + left_keys_sprawl - left_keys_size / 2,
                                         window_height / 2 - left_keys_size / 2,
                                         left_keys_size, left_keys_size))
        self.btn_down = QPushButton(self)
        self.btn_down.setText('D')
        self.btn_down.setGeometry(QRect(left_keys_x_pos - left_keys_size / 2,
                                        window_height / 2 + left_keys_sprawl - left_keys_size / 2,
                                        left_keys_size, left_keys_size))
        self.btn_left = QPushButton(self)
        self.btn_left.setText('L')
        self.btn_left.setGeometry(QRect(left_keys_x_pos - left_keys_sprawl - left_keys_size / 2,
                                        window_height / 2 - left_keys_size / 2,
                                        left_keys_size, left_keys_size))
        self.btn_press = QPushButton(self)
        self.btn_press.setText('P')
        self.btn_press.setGeometry(QRect(left_keys_x_pos - left_keys_size / 2,
                                         window_height / 2 - left_keys_size / 2,
                                         left_keys_size, left_keys_size))
        self.btn_1 = QPushButton(self)
        self.btn_1.setText('1')
        self.btn_1.setGeometry(QRect(RK_XPOS - right_keys_x_size / 2,
                                     window_height / 2 - right_keys_y_size / 2 - right_keys_sprawl,
                                     right_keys_x_size, right_keys_y_size))
        self.btn_2 = QPushButton(self)
        self.btn_2.setText('2')
        self.btn_2.setGeometry(QRect(RK_XPOS - right_keys_x_size / 2,
                                     window_height / 2 - right_keys_y_size / 2,
                                     right_keys_x_size, right_keys_y_size))
        self.btn_3 = QPushButton(self)
        self.btn_3.setText('3')
        self.btn_3.setGeometry(QRect(RK_XPOS - right_keys_x_size / 2,
                                     window_height / 2 - right_keys_y_size / 2 + right_keys_sprawl,
                                     right_keys_x_size, right_keys_y_size))
        self.label = QLabel(self)
        self.q_img = ImageQt.ImageQt(Image.new('RGB', (240, 240), (0, 0, 0)))
        self.pixmap = QPixmap.fromImage(self.q_img)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(QRect(SC_XPOS - 120,
                                     window_height / 2 - 120,
                                     240, 240))


app = QApplication(sys.argv)
emulator_window = EmulatorWindow()


def on_key_up():
    page_switcher.on_key_up()


def on_key_right():
    page_switcher.on_key_right()


def on_key_down():
    page_switcher.on_key_down()


def on_key_left():
    page_switcher.on_key_left()


def on_key_press():
    page_switcher.on_key_press()


def on_key_1():
    page_switcher.on_key_1()


def on_key_2():
    page_switcher.on_key_2()


def on_key_3():
    page_switcher.on_key_3()


emulator_window.btn_up.clicked.connect(on_key_up)
emulator_window.btn_right.clicked.connect(on_key_right)
emulator_window.btn_down.clicked.connect(on_key_down)
emulator_window.btn_left.clicked.connect(on_key_left)
emulator_window.btn_press.clicked.connect(on_key_press)
emulator_window.btn_1.clicked.connect(on_key_1)
emulator_window.btn_2.clicked.connect(on_key_2)
emulator_window.btn_3.clicked.connect(on_key_3)


class EmulatorCapabilities(ProtoDeviceCapabilities):
    def update_screen(self, image):
        emulator_window.q_img = ImageQt.ImageQt(image)
        emulator_window.pixmap = QPixmap.fromImage(emulator_window.q_img)
        emulator_window.label.setPixmap(emulator_window.pixmap)

    def get_ip_addr(self):
        return '---.---.---.---'

    def socket_command(self, command):
        return None


emulator_capabilities = EmulatorCapabilities()


def tick_service():
    while True:
        time.sleep(time.time() % TICK_INTERVAL)
        page_switcher.on_tick(emulator_capabilities)


tick_thread = threading.Thread(target=tick_service, daemon=True)
tick_thread.start()

emulator_window.show()
sys.exit(app.exec_())
