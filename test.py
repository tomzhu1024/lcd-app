import time

from PIL import Image

from device_io.raspberry_pi import RaspberryPi

pi = RaspberryPi()

pi.connect_button_up_pressed_handler(lambda: print('up pressed'))
pi.connect_button_up_released_handler(lambda: print('up released'))

pi.connect_button_down_pressed_handler(lambda: print('down pressed'))
pi.connect_button_down_released_handler(lambda: print('down released'))

pi.connect_button_left_pressed_handler(lambda: print('left pressed'))
pi.connect_button_left_released_handler(lambda: print('left released'))

pi.connect_button_right_pressed_handler(lambda: print('right pressed'))
pi.connect_button_right_released_handler(lambda: print('right released'))

pi.connect_button_center_pressed_handler(lambda: print('center pressed'))
pi.connect_button_center_released_handler(lambda: print('center released'))

pi.connect_button_1_pressed_handler(lambda: print('1 pressed'))
pi.connect_button_1_released_handler(lambda: print('1 released'))

pi.connect_button_2_pressed_handler(lambda: print('2 pressed'))
pi.connect_button_2_released_handler(lambda: print('2 released'))

pi.connect_button_3_pressed_handler(lambda: print('3 pressed'))
pi.connect_button_3_released_handler(lambda: print('3 released'))

img = Image.new('RGB', (240, 240), (255, 100, 50))
pi.update_display(img)
while True:
    print('sleep')
    time.sleep(5)
