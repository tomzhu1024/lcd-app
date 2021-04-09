from threading import Lock

from PIL import Image, ImageDraw, ImageFont

from clock import Clock
from shared_utils import centered_text, regular_polygon
from system_info import SystemInfo

# style
page_indicator_color = (200, 200, 200)
page_indicator_font = ImageFont.truetype('fonts/noto-regular.otf', size=14)

pages = [
    Clock(),
    SystemInfo()
]
current_page = 0
previous_page = 0
total_page = len(pages)
need_page_switch = False
first_tick = True

lock = Lock()


def on_key_left():
    lock.acquire()
    global current_page, previous_page, need_page_switch
    previous_page = current_page
    current_page -= 1
    if current_page < 0:
        current_page += total_page
    need_page_switch = True
    lock.release()


def on_key_right():
    lock.acquire()
    global current_page, previous_page, need_page_switch
    previous_page = current_page
    current_page += 1
    if current_page >= total_page:
        current_page -= total_page
    need_page_switch = True
    lock.release()


def on_key_up():
    lock.acquire()
    pages[current_page].on_key_up()
    lock.release()


def on_key_down():
    lock.acquire()
    pages[current_page].on_key_down()
    lock.release()


def on_key_press():
    lock.acquire()
    pages[current_page].on_key_press()
    lock.release()


def on_key_1():
    lock.acquire()
    pages[current_page].on_key_1()
    lock.release()


def on_key_2():
    lock.acquire()
    pages[current_page].on_key_2()
    lock.release()


def on_key_3():
    lock.acquire()
    pages[current_page].on_key_3()
    lock.release()


def on_tick(device_capabilities):
    lock.acquire()
    global need_page_switch, first_tick
    fg_tick = pages[current_page].on_foreground_tick(device_capabilities)
    for i in range(len(pages)):
        if i != current_page:
            pages[i].on_background_tick(device_capabilities)
    if first_tick:
        first_tick = False
        pages[current_page].on_page_load()
    if need_page_switch or fg_tick:
        if need_page_switch:
            pages[previous_page].on_page_unload()
            pages[current_page].on_page_load()
            need_page_switch = False
        image = Image.new('RGB', (240, 240), (0, 0, 0))
        pages[current_page].render(image)
        draw = ImageDraw.Draw(image)
        text = '%s - %d/%d' % (pages[current_page].display_name,
                               current_page + 1,
                               total_page)
        centered_text(draw, 120, 226, text, page_indicator_color, page_indicator_font)
        w, h = draw.textsize(text, page_indicator_font)
        regular_polygon(draw, 110 - w / 2, 229, 5, 3, 180, page_indicator_color, None)
        regular_polygon(draw, 130 + w / 2, 229, 5, 3, 0, page_indicator_color, None)
        device_capabilities.update_screen(image)
    lock.release()
