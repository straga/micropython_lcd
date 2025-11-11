import gt911
import i2c
import lcd_bus
import lvgl as lv  # NOQA
import machine

from micropython import const

import nv3041aG as nv3041a  # NOQA


WIDTH = 480
HEIGHT = 272

_WIDTH = const(480)
_HEIGHT = const(272)

_BUFFER_SIZE = _WIDTH * _HEIGHT * 2


_RTP_CS = const(10)
_RTP_MISO = const(13)
_RTP_CLK = const(12)
_RTP_MOSI = const(11)
_RTP_IRQ = const(3)
_RTP_FREQ = const(10000000)
_RTP_HOST = const(1)


_SPECK_DIN = const(41)
_SPECK_BCLK = const(42)
_SPECK_LRCLK = const(2)


_LCD_TE = const(0)  # not used
_LCD_BL = const(1)
_LCD_CS = const(45)
_LCD_CLK = const(47)
_LCD_A0 = const(21)
_LCD_A1 = const(48)
_LCD_A2 = const(40)
_LCD_A3 = const(39)
_LCD_HOST = const(2)
_LCD_FREQ = const(32000000)

#
# // LCD backlight PWM
# #define LCD_BL 1           // lcd BL pin
# #define LEDC_CHANNEL_0     0 // use first channel of 16 channels (started from zero)
# #define LEDC_TIMER_12_BIT  12 // use 12 bit precission for LEDC timer
# #define LEDC_BASE_FREQ     5000 // use 5000 Hz as a LEDC base frequency


disp_spi_bus = machine.SPI.Bus(
    host=_LCD_HOST,
    mosi=_LCD_A0,
    miso=_LCD_A1,
    sck=_LCD_CLK,
    quad_pins=(_LCD_A0, _LCD_A1, _LCD_A2, _LCD_A3), # quad wait 4 arguments
)

display_bus = lcd_bus.SPIBus(
    spi_bus=disp_spi_bus, dc=-1, freq=_LCD_FREQ, cs=_LCD_CS, quad=True
)

fb1 = display_bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)


display = nv3041a.NV3041A(
    data_bus=display_bus,
    frame_buffer1=fb1,
    frame_buffer2=None,
    display_width=_WIDTH,
    display_height=_HEIGHT,
    backlight_pin=_LCD_BL,
    backlight_on_state=nv3041a.STATE_PWM,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True,
)


display.set_power(True)
# display.set_backlight(100)
display.init(3)

# PWM frequency for backlight
display._backlight_pin.freq(5000)
display.set_backlight(80)


TOUCH_SCL = 4
TOUCH_SDA = 8
TOUCH_RES = 38
TOUCH_INT = 3

i2c_bus = i2c.I2C.Bus(host=1, scl=TOUCH_SCL, sda=TOUCH_SDA, use_locks=True)
touch_i2c = i2c.I2C.Device(i2c_bus, gt911.I2C_ADDR, gt911.BITS)
indev = gt911.GT911(touch_i2c, debug=False)
indev.enable_input_priority()
