from typing import Callable

from PIL import Image


class Prototype:
    """Class for prototype device inputs and outputs."""

    def __init__(self):
        # button pressed events
        self._button_up_pressed_handler = None
        self._button_down_pressed_handler = None
        self._button_left_pressed_handler = None
        self._button_right_pressed_handler = None
        self._button_center_pressed_handler = None
        self._button_1_pressed_handler = None
        self._button_2_pressed_handler = None
        self._button_3_pressed_handler = None
        # button released events
        self._button_up_released_handler = None
        self._button_down_released_handler = None
        self._button_left_released_handler = None
        self._button_right_released_handler = None
        self._button_center_released_handler = None
        self._button_1_released_handler = None
        self._button_2_released_handler = None
        self._button_3_released_handler = None

    def _on_button_up_pressed(self, *_):
        if self._button_up_pressed_handler is not None:
            self._button_up_pressed_handler()

    def _on_button_down_pressed(self, *_):
        if self._button_down_pressed_handler is not None:
            self._button_down_pressed_handler()

    def _on_button_left_pressed(self, *_):
        if self._button_left_pressed_handler is not None:
            self._button_left_pressed_handler()

    def _on_button_right_pressed(self, *_):
        if self._button_right_pressed_handler is not None:
            self._button_right_pressed_handler()

    def _on_button_center_pressed(self, *_):
        if self._button_center_pressed_handler is not None:
            self._button_center_pressed_handler()

    def _on_button_1_pressed(self, *_):
        if self._button_1_pressed_handler is not None:
            self._button_1_pressed_handler()

    def _on_button_2_pressed(self, *_):
        if self._button_2_pressed_handler is not None:
            self._button_2_pressed_handler()

    def _on_button_3_pressed(self, *_):
        if self._button_3_pressed_handler is not None:
            self._button_3_pressed_handler()

    def _on_button_up_released(self, *_):
        if self._button_up_released_handler is not None:
            self._button_up_released_handler()

    def _on_button_down_released(self, *_):
        if self._button_down_released_handler is not None:
            self._button_down_released_handler()

    def _on_button_left_released(self, *_):
        if self._button_left_released_handler is not None:
            self._button_left_released_handler()

    def _on_button_right_released(self, *_):
        if self._button_right_released_handler is not None:
            self._button_right_released_handler()

    def _on_button_center_released(self, *_):
        if self._button_center_released_handler is not None:
            self._button_center_released_handler()

    def _on_button_1_released(self, *_):
        if self._button_1_released_handler is not None:
            self._button_1_released_handler()

    def _on_button_2_released(self, *_):
        if self._button_2_released_handler is not None:
            self._button_2_released_handler()

    def _on_button_3_released(self, *_):
        if self._button_3_released_handler is not None:
            self._button_3_released_handler()

    def connect_button_up_pressed_handler(self, handler: Callable[[], None]):
        self._button_up_pressed_handler = handler

    def connect_button_down_pressed_handler(self, handler: Callable[[], None]):
        self._button_down_pressed_handler = handler

    def connect_button_left_pressed_handler(self, handler: Callable[[], None]):
        self._button_left_pressed_handler = handler

    def connect_button_right_pressed_handler(self, handler: Callable[[], None]):
        self._button_right_pressed_handler = handler

    def connect_button_center_pressed_handler(self, handler: Callable[[], None]):
        self._button_center_pressed_handler = handler

    def connect_button_1_pressed_handler(self, handler: Callable[[], None]):
        self._button_1_pressed_handler = handler

    def connect_button_2_pressed_handler(self, handler: Callable[[], None]):
        self._button_2_pressed_handler = handler

    def connect_button_3_pressed_handler(self, handler: Callable[[], None]):
        self._button_3_pressed_handler = handler

    def connect_button_up_released_handler(self, handler: Callable[[], None]):
        self._button_up_released_handler = handler

    def connect_button_down_released_handler(self, handler: Callable[[], None]):
        self._button_down_released_handler = handler

    def connect_button_left_released_handler(self, handler: Callable[[], None]):
        self._button_left_released_handler = handler

    def connect_button_right_released_handler(self, handler: Callable[[], None]):
        self._button_right_released_handler = handler

    def connect_button_center_released_handler(self, handler: Callable[[], None]):
        self._button_center_released_handler = handler

    def connect_button_1_released_handler(self, handler: Callable[[], None]):
        self._button_1_released_handler = handler

    def connect_button_2_released_handler(self, handler: Callable[[], None]):
        self._button_2_released_handler = handler

    def connect_button_3_released_handler(self, handler: Callable[[], None]):
        self._button_3_released_handler = handler

    def update_display(self, image: Image):
        pass


__all__ = ['Prototype']
