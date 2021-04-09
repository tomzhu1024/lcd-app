from PIL import ImageDraw, ImageFont

from shared_utils import ProtoPage, IntervalScheduler

# style
label_font = ImageFont.truetype('fonts/noto-regular.otf', size=18)
info_font = ImageFont.truetype('fonts/noto-bold.otf', size=18)
label_color = (255, 255, 255)
yellow_color = (245, 252, 7)
blue_color = (9, 251, 247)


class SystemInfo(ProtoPage):
    def __init__(self):
        super().__init__()
        self._display_name = '系统'

        self._scheduler = IntervalScheduler(3)
        self._ip_addr = None
        self._battery = None
        self._battery_i = None
        self._power_plugged = None
        self._power_plugged_color = yellow_color
        self._allow_charging = None
        self._allow_charging_color = yellow_color

    def on_foreground_tick(self, device_capabilities):
        need_render = False
        if self._scheduler.tick():
            # ip_addr
            ip_addr = device_capabilities.get_ip_addr()
            if self._ip_addr != ip_addr:
                self._ip_addr = ip_addr
                need_render = True
            # battery
            battery = device_capabilities.socket_command('get battery')
            if battery is not None:
                battery = '%.2f%%' % float(battery)
            else:
                battery = '--%'
            if self._battery != battery:
                self._battery = battery
                need_render = True
            # battery_i
            battery_i = device_capabilities.socket_command('get battery_i')
            if battery_i is not None:
                battery_i = '%.2fA' % float(battery_i)
            else:
                battery_i = '--A'
            if self._battery_i != battery_i:
                self._battery_i = battery_i
                need_render = True
            # power_plugged
            power_plugged = device_capabilities.socket_command('get battery_power_plugged')
            if power_plugged is not None:
                self._power_plugged_color = blue_color if power_plugged == 'true' else yellow_color
                power_plugged = '已接通' if power_plugged == 'true' else '未接通'
            else:
                self._power_plugged_color = yellow_color
                power_plugged = '---'
            if self._power_plugged != power_plugged:
                self._power_plugged = power_plugged
                need_render = True
            # allow_charging
            allow_charging = device_capabilities.socket_command('get battery_allow_charging')
            if allow_charging is not None:
                self._allow_charging_color = blue_color if allow_charging == 'true' else yellow_color
                allow_charging = '是' if allow_charging == 'true' else '否'
            else:
                self._allow_charging_color = yellow_color
                allow_charging = '---'
            if self._allow_charging != allow_charging:
                self._allow_charging = allow_charging
                need_render = True
        return need_render

    def render(self, image):
        draw = ImageDraw.Draw(image)
        draw.text((10, 30), '本机地址：', fill=label_color, font=label_font)
        draw.text((10, 60), '电池电量：', fill=label_color, font=label_font)
        draw.text((10, 90), '电池电流：', fill=label_color, font=label_font)
        draw.text((10, 120), '外接电源：', fill=label_color, font=label_font)
        draw.text((10, 150), '允许充电：', fill=label_color, font=label_font)
        draw.text((95, 30), self._ip_addr, fill=label_color, font=info_font)
        draw.text((95, 60), self._battery, fill=label_color, font=info_font)
        draw.text((95, 90), self._battery_i, fill=label_color, font=info_font)
        draw.text((95, 120), self._power_plugged, fill=self._power_plugged_color, font=info_font)
        draw.text((95, 150), self._allow_charging, fill=self._allow_charging_color, font=info_font)
