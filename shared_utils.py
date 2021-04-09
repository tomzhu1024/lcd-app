import math
import time


class ProtoDeviceCapabilities:
    def update_screen(self, image):
        raise NotImplementedError()

    def get_ip_addr(self):
        raise NotImplementedError()

    def socket_command(self, command):
        raise NotImplementedError()


class ProtoPage:
    def __init__(self):
        self._display_name = ''

    @property
    def display_name(self):
        return self._display_name

    def on_page_load(self):
        pass

    def on_page_unload(self):
        pass

    def on_foreground_tick(self, device_capabilities):
        return False

    def on_background_tick(self, device_capabilities):
        pass

    def on_key_up(self):
        pass

    def on_key_down(self):
        pass

    def on_key_left(self):
        pass

    def on_key_right(self):
        pass

    def on_key_press(self):
        pass

    def on_key_1(self):
        pass

    def on_key_2(self):
        pass

    def on_key_3(self):
        pass

    def render(self, image):
        pass


class IntervalScheduler:
    def __init__(self, interval):
        self._interval = interval
        self._last_hit = -1

    def tick(self):
        cur = time.time()
        if cur - self._last_hit >= self._interval:
            self._last_hit = cur
            return True
        else:
            return False


def centered_text(draw, left, top, text, fill, font):
    w, h = draw.textsize(text, font=font)
    draw.text((left - w / 2, top - h / 2), text, fill=fill, font=font)


def regular_polygon(draw, x, y, r, sides, rotate, fill=None, outline=None):
    rotate = rotate / 180 * math.pi
    draw.polygon(tuple(
        (
            x + r * math.cos(rotate + 2 * math.pi / sides * i),
            y + r * math.sin(rotate + 2 * math.pi / sides * i)
        ) for i in range(sides)),
        fill=fill, outline=outline)
