from datetime import datetime, timedelta

from PIL import ImageDraw, ImageFont

from shared_utils import ProtoPage, centered_text, IntervalScheduler

# style
time_font = ImageFont.truetype('fonts/noto-bold.otf', size=56)
date_font = ImageFont.truetype('fonts/noto-regular.otf', size=22)
hint_font = ImageFont.truetype('fonts/noto-regular.otf', size=16)

time_color = (0, 255, 255)
date_color = (200, 200, 0)

week_day_table = {
    0: '周一',
    1: '周二',
    2: '周三',
    3: '周四',
    4: '周五',
    5: '周六',
    6: '周日',
}


class Clock(ProtoPage):
    def __init__(self):
        super().__init__()
        self._display_name = '时钟'

        self._rtc_sync_scheduler = IntervalScheduler(10)
        self._time_offset = timedelta(seconds=0)
        self._year = 1970
        self._month = 1
        self._day = 1
        self._week_day = 1
        self._hour = 0
        self._minute = 0
        self._second = 0
        self._rtc_status = 0  # 0 is error, 1 is disabled, 2 is enabled

    def on_foreground_tick(self, device_capabilities):
        need_render = False
        if self._rtc_sync_scheduler.tick():
            try:
                now = datetime.now()
                rtc = datetime.strptime(device_capabilities.socket_command('get rtc_time'),
                                        "%Y-%m-%dT%H:%M:%S+08:00")
                self._time_offset = rtc - now
                print(abs(self._time_offset.total_seconds()))
                if abs(self._time_offset.total_seconds()) < 5:
                    rtc_status = 1
                    self._time_offset = timedelta(seconds=0)
                else:
                    rtc_status = 2
            except:
                self._time_offset = timedelta(seconds=0)
                rtc_status = 0
            if self._rtc_status != rtc_status:
                self._rtc_status = rtc_status
                need_render = True
        current_datetime = datetime.now() + self._time_offset
        if self._year != current_datetime.date().year:
            self._year = current_datetime.date().year
            need_render = True
        if self._month != current_datetime.date().month:
            self._month = current_datetime.date().month
            need_render = True
        if self._day != current_datetime.date().day:
            self._day = current_datetime.date().day
            need_render = True
        if self._week_day != current_datetime.date().weekday():
            self._week_day = current_datetime.date().weekday()
            need_render = True
        if self._hour != current_datetime.time().hour:
            self._hour = current_datetime.time().hour
            need_render = True
        if self._minute != current_datetime.time().minute:
            self._minute = current_datetime.time().minute
            need_render = True
        if self._second != current_datetime.time().second:
            self._second = current_datetime.time().second
            need_render = True
        return need_render

    def render(self, image):
        draw = ImageDraw.Draw(image)
        centered_text(draw, 120, 75, '%02d:%02d:%02d' % (self._hour, self._minute, self._second),
                      time_color, time_font)
        centered_text(draw, 120, 155,
                      '%04d年%02d月%02d日 %s' % (self._year, self._month, self._day, week_day_table[self._week_day]),
                      date_color, date_font)
        if self._rtc_status == 0:
            centered_text(draw, 120, 15, '系统时钟优先/RTC错误', (200, 0, 0), hint_font)
        elif self._rtc_status == 1:
            centered_text(draw, 120, 15, '系统时钟优先/RTC正常', (0, 200, 0),
                          hint_font)
        else:
            centered_text(draw, 120, 15, 'RTC校准已启用 (%.3f秒)' % self._time_offset.total_seconds(), (0, 200, 0),
                          hint_font)
