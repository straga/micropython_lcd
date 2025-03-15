# Based on the work by straga (https://github.com/straga)
# https://github.com/straga/micropython_lcd/blob/master/device/JC3248W535/driver/axs15231b/axs15231b.py
# Copyright (c) 2024 - 2025 Kevin G. Schlosser


import display_driver_framework
from micropython import const  # NOQA

import lcd_bus
import gc

import lvgl as lv  # NOQA

STATE_HIGH = display_driver_framework.STATE_HIGH
STATE_LOW = display_driver_framework.STATE_LOW
STATE_PWM = display_driver_framework.STATE_PWM

BYTE_ORDER_RGB = display_driver_framework.BYTE_ORDER_RGB
BYTE_ORDER_BGR = display_driver_framework.BYTE_ORDER_BGR

_WRITE_CMD = const(0x02)
_WRITE_COLOR = const(0x32)

_MADCTL_MH = const(0x04)  # Refresh 0=Left to Right, 1=Right to Left
_MADCTL_BGR = const(0x08)  # BGR color order
_MADCTL_ML = const(0x10)  # Refresh 0=Top to Bottom, 1=Bottom to Top

_MADCTL_MV = const(0x20)  # 0=Normal, 1=Row/column exchange
_MADCTL_MX = const(0x40)  # 0=Left to Right, 1=Right to Left
_MADCTL_MY = const(0x80)  # 0=Top to Bottom, 1=Bottom to Top

_RASET = const(0x2B)
_CASET = const(0x2A)
_RAMWR = const(0x2C)
_RAMWRC = const(0x3C)
_MADCTL = const(0x36)

import nv3041aG

class AXS15231B(nv3041aG.NV3041A):

    _brightness = 0xD0

    def set_rotation(self, value):
        if not isinstance(self._data_bus, lcd_bus.RGBBus):
            raise NotImplementedError

        super().set_rotation(value)

    def set_brightness(self, value):
        value = int(value / 100.0 * 255)
        value = max(0x00, min(value, 0xFF))

        self._brightness = value

        self._param_buf[0] = value
        self.set_params(_WRDISBV, self._param_mv[:1])

    def get_brightness(self):
        return round(self._brightness / 255.0 * 100.0, 1)


