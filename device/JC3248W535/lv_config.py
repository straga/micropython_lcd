
from micropython import const # NOQA

import lcd_bus # NOQA
from machine import SPI, Pin # NOQA

import lvgl as lv # NOQA

WIDTH = const(320)
HEIGHT = const(480)

_WIDTH = const(320)
_HEIGHT = const(480)

_BUFFER_SIZE = _WIDTH * _HEIGHT * 2


## Panel

# LCD_QSPI_HOST           (SPI2_HOST)     SPI2_HOST=1, ok

# PIN_NUM_QSPI_CS         (GPIO_NUM_45) ok
# PIN_NUM_QSPI_PCLK       (GPIO_NUM_47) ok

# PIN_NUM_QSPI_DATA0      (GPIO_NUM_21) ok
# PIN_NUM_QSPI_DATA1      (GPIO_NUM_48) ok
# PIN_NUM_QSPI_DATA2      (GPIO_NUM_40) ok
# PIN_NUM_QSPI_DATA3      (GPIO_NUM_39) ok

# PIN_NUM_QSPI_RST        (GPIO_NUM_NC) NC
# PIN_NUM_QSPI_DC         (GPIO_NUM_8) ok
# PIN_NUM_QSPI_TE         (GPIO_NUM_38)
# PIN_NUM_QSPI_BL         (GPIO_NUM_1) ok

## Touch

# I2C_NUM                     (I2C_NUM_0) ok
# I2C_CLK_SPEED_HZ            400000 ok

# PIN_NUM_QSPI_TOUCH_SCL  (GPIO_NUM_8) ok
# PIN_NUM_QSPI_TOUCH_SDA  (GPIO_NUM_4) ok
# PIN_NUM_QSPI_TOUCH_RST  (-1)
# PIN_NUM_QSPI_TOUCH_INT  (-1)



# SPI bus config
spi_bus = SPI.Bus(
    host=1,   # SPI2_HOST
    mosi=21,  # PIN_NUM_QSPI_DATA0
    miso=48,  # PIN_NUM_QSPI_DATA1
    sck=47,   # PIN_NUM_QSPI_PCLK
    quad_pins=(40, 39)  # PIN_NUM_QSPI_DATA2, PIN_NUM_QSPI_DATA3
)

# Display bus config
display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    dc=8,  # PIN_NUM_QSPI_DC 8
    cs=45,  # PIN_NUM_QSPI_CS
    freq=40000000,
    spi_mode=0,
    quad=True
)

import axs15231b


fb1 = display_bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)
fb2 = display_bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)


display = axs15231b.AXS15231B(
    display_bus,
    WIDTH,
    HEIGHT,
    frame_buffer1=fb1,
    frame_buffer2=fb1,
    backlight_pin=1,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True,
    backlight_on_state=axs15231b.STATE_PWM
)


print('Hello LCD')
print(f"Display size: {WIDTH}x{HEIGHT}")

display.set_power(True)
display.set_backlight(80)
# PWM frequency for backlight
#display._backlight_pin.freq(2000)

display.init()  # use 1 type config

#display.set_rotation(lv.DISPLAY_ROTATION._90)  # NOQA


# TOUCH

# I2C_NUM_0
# I2C_CLK_SPEED_HZ            400000

# PIN_NUM_QSPI_TOUCH_SCL  (GPIO_NUM_8)
# PIN_NUM_QSPI_TOUCH_SDA  (GPIO_NUM_4)

import axs15231
from i2c import I2C

i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, axs15231.I2C_ADDR, axs15231.BITS)
indev = axs15231.AXS15231(touch_i2c, debug=False)
indev.enable_input_priority()

print('is_calibrate is', indev.is_calibrated)

