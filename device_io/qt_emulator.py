import sys

from PIL import Image, ImageQt
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QDesktopWidget

from ._prototype import Prototype

# window style
window_width = 575
window_height = 260
left_keys_size = 50
left_keys_sprawl = 50
right_keys_x_size = 120
right_keys_y_size = 55
right_keys_sprawl = 60
left_keys_x_pos = (window_width / 2 - 120) / 2
screen_x_pos = window_width / 2
right_keys_x_pos = window_width - left_keys_x_pos

# refresh rate
TICK_INTERVAL = 0.1


class EmulatorWindow(QWidget):
    """Class for Qt emulator windows."""

    def __init__(self):
        super().__init__()
        self._screen_width = 240
        self._screen_height = 240

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(QRect(screen.width() / 2 - window_width / 2,
                               screen.height() / 2 - window_height / 2,
                               window_width, window_height))
        self.setWindowTitle('Emulator')
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.btn_up = QPushButton(self)
        self.btn_up.setText('U')
        self.btn_up.setGeometry(QRect(left_keys_x_pos - left_keys_size / 2,
                                      window_height / 2 - left_keys_sprawl - left_keys_size / 2,
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
        self.btn_right = QPushButton(self)
        self.btn_right.setText('R')
        self.btn_right.setGeometry(QRect(left_keys_x_pos + left_keys_sprawl - left_keys_size / 2,
                                         window_height / 2 - left_keys_size / 2,
                                         left_keys_size, left_keys_size))
        self.btn_center = QPushButton(self)
        self.btn_center.setText('C')
        self.btn_center.setGeometry(QRect(left_keys_x_pos - left_keys_size / 2,
                                          window_height / 2 - left_keys_size / 2,
                                          left_keys_size, left_keys_size))
        self.btn_1 = QPushButton(self)
        self.btn_1.setText('1')
        self.btn_1.setGeometry(QRect(right_keys_x_pos - right_keys_x_size / 2,
                                     window_height / 2 - right_keys_y_size / 2 - right_keys_sprawl,
                                     right_keys_x_size, right_keys_y_size))
        self.btn_2 = QPushButton(self)
        self.btn_2.setText('2')
        self.btn_2.setGeometry(QRect(right_keys_x_pos - right_keys_x_size / 2,
                                     window_height / 2 - right_keys_y_size / 2,
                                     right_keys_x_size, right_keys_y_size))
        self.btn_3 = QPushButton(self)
        self.btn_3.setText('3')
        self.btn_3.setGeometry(QRect(right_keys_x_pos - right_keys_x_size / 2,
                                     window_height / 2 - right_keys_y_size / 2 + right_keys_sprawl,
                                     right_keys_x_size, right_keys_y_size))
        self.label = QLabel(self)
        self.q_img = ImageQt.ImageQt(Image.new('RGB', (self._screen_width, self._screen_height), (0, 0, 0)))
        self.pixmap = QPixmap.fromImage(self.q_img)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(QRect(screen_x_pos - 120,
                                     window_height / 2 - 120,
                                     240, 240))

    def show_image(self, image):
        # check image size
        im_width, im_height = image.size
        if im_width != self._screen_width or im_height != self._screen_height:
            raise ValueError(
                'Image must be same dimensions as display ({0}x{1}).'.format(self._screen_width, self._screen_height))
        self.q_img = ImageQt.ImageQt(image)
        self.pixmap = QPixmap.fromImage(self.q_img)
        self.label.setPixmap(self.pixmap)


class QtEmulator(Prototype):
    """Class for Qt emulator device inputs and outputs."""

    def __init__(self):
        super().__init__()
        # emulator window
        self._app = QApplication(sys.argv)
        self._emulator_window = EmulatorWindow()
        # connect button pressed slots
        self._emulator_window.btn_up.pressed.connect(self._on_button_up_pressed)
        self._emulator_window.btn_down.pressed.connect(self._on_button_down_pressed)
        self._emulator_window.btn_left.pressed.connect(self._on_button_left_pressed)
        self._emulator_window.btn_right.pressed.connect(self._on_button_right_pressed)
        self._emulator_window.btn_center.pressed.connect(self._on_button_center_pressed)
        self._emulator_window.btn_1.pressed.connect(self._on_button_1_pressed)
        self._emulator_window.btn_2.pressed.connect(self._on_button_2_pressed)
        self._emulator_window.btn_3.pressed.connect(self._on_button_3_pressed)
        # connect button released slots
        self._emulator_window.btn_up.released.connect(self._on_button_up_released)
        self._emulator_window.btn_down.released.connect(self._on_button_down_released)
        self._emulator_window.btn_left.released.connect(self._on_button_left_released)
        self._emulator_window.btn_right.released.connect(self._on_button_right_released)
        self._emulator_window.btn_center.released.connect(self._on_button_center_released)
        self._emulator_window.btn_1.released.connect(self._on_button_1_released)
        self._emulator_window.btn_2.released.connect(self._on_button_2_released)
        self._emulator_window.btn_3.released.connect(self._on_button_3_released)

    def show(self):
        """Show the emulator window and block."""
        self._emulator_window.show()
        sys.exit(self._app.exec_())

    def update_display(self, image: Image):
        self._emulator_window.show_image(image)


__all__ = ['QtEmulator']
