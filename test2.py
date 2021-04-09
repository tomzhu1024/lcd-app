import threading
import time

from PIL import Image

from device_io.qt_emulator import QtEmulator

emu = QtEmulator()

emu.connect_button_up_pressed_handler(lambda: print('qt up pressed'))
emu.connect_button_up_released_handler(lambda: print('qt up released'))

emu.connect_button_down_pressed_handler(lambda: print('qt down pressed'))
emu.connect_button_down_released_handler(lambda: print('qt down released'))

emu.connect_button_left_pressed_handler(lambda: print('qt left pressed'))
emu.connect_button_left_released_handler(lambda: print('qt left released'))

emu.connect_button_right_pressed_handler(lambda: print('qt right pressed'))
emu.connect_button_right_released_handler(lambda: print('qt right released'))

emu.connect_button_center_pressed_handler(lambda: print('qt center pressed'))
emu.connect_button_center_released_handler(lambda: print('qt center released'))

emu.connect_button_1_pressed_handler(lambda: print('qt 1 pressed'))
emu.connect_button_1_released_handler(lambda: print('qt 1 released'))

emu.connect_button_2_pressed_handler(lambda: print('qt 2 pressed'))
emu.connect_button_2_released_handler(lambda: print('qt 2 released'))

emu.connect_button_3_pressed_handler(lambda: print('qt 3 pressed'))
emu.connect_button_3_released_handler(lambda: print('qt 3 released'))


def worker():
    time.sleep(6)
    emu.update_display(Image.new('RGB', (240, 240), (255, 100, 50)))
    time.sleep(6)


th = threading.Thread(target=worker, daemon=False)
th.start()

emu.show()
