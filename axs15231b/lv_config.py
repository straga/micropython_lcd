
from micropython import const # NOQA

WIDTH = const(320)
HEIGHT = const(480)


import lcd_bus # NOQA
from machine import SPI, Pin # NOQA

import lvgl as lv # NOQA

# BUFFER_SIZE = int(WIDTH * HEIGHT) * 2
# BUFFER_SIZE = int(BUFFER_SIZE // 10)


## Panel

# LCD_QSPI_HOST           (SPI2_HOST)     SPI2_HOST=1,

# PIN_NUM_QSPI_CS         (GPIO_NUM_45) ok
# PIN_NUM_QSPI_PCLK       (GPIO_NUM_47) ok

# PIN_NUM_QSPI_DATA0      (GPIO_NUM_21) ok
# PIN_NUM_QSPI_DATA1      (GPIO_NUM_48) ok
# PIN_NUM_QSPI_DATA2      (GPIO_NUM_40) ok
# PIN_NUM_QSPI_DATA3      (GPIO_NUM_39) ok

# PIN_NUM_QSPI_RST        (GPIO_NUM_NC)
# PIN_NUM_QSPI_DC         (GPIO_NUM_8) ok
# PIN_NUM_QSPI_TE         (GPIO_NUM_38)
# PIN_NUM_QSPI_BL         (GPIO_NUM_1) ok

## Touch

# I2C_NUM                     (I2C_NUM_0)
# I2C_CLK_SPEED_HZ            400000

# PIN_NUM_QSPI_TOUCH_SCL  (GPIO_NUM_8)
# PIN_NUM_QSPI_TOUCH_SDA  (GPIO_NUM_4)
# PIN_NUM_QSPI_TOUCH_RST  (-1)
# PIN_NUM_QSPI_TOUCH_INT  (-1)

'''
config from C code
{                                                          
    .cs_gpio_num = cs,                                     
    .dc_gpio_num = -1,                                      
    .spi_mode = 3,                                         
    .pclk_hz = 40 * 1000 * 1000,                           
    .trans_queue_depth = 10,                                                                
    .lcd_cmd_bits = 32,                                     
    .lcd_param_bits = 8,                                                     
    .quad_mode = true,                                 
                                                   
}
'''

# SPI bus config
spi_bus = SPI.Bus(
    host=1,   # SPI2_HOST
    mosi=21,  # PIN_NUM_QSPI_DATA0
    miso=48,  # PIN_NUM_QSPI_DATA1
    sck=47,   # PIN_NUM_QSPI_PCLK
    quad_pins=(40, 39),  # PIN_NUM_QSPI_DATA2, PIN_NUM_QSPI_DATA3
)


# Display bus config
'''
{
    ARG_spi_bus,
    ARG_dc,
    ARG_freq,
    ARG_cs,
    ARG_dc_low_on_data,
    ARG_lsb_first,
    ARG_cs_high_active,
    ARG_spi_mode,
    ARG_dual,
    ARG_quad,
    ARG_octal
};
'''
display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    dc=8,  # PIN_NUM_QSPI_DC 8
    cs=45,  # PIN_NUM_QSPI_CS
    freq=40000000,
    spi_mode=3,
    quad=True
)

import axs15231b

## Default config
# data_bus,
# display_width,
# display_height,
# frame_buffer1 = None,
# frame_buffer2 = None,
# reset_pin = None,
# reset_state = STATE_HIGH,
# power_pin = None,
# power_on_state = STATE_HIGH,
# backlight_pin = None,
# backlight_on_state = STATE_HIGH,
# offset_x = 0,
# offset_y = 0,
# color_byte_order = BYTE_ORDER_RGB,
# color_space = lv.COLOR_FORMAT.RGB888,  # NOQA
# rgb565_byte_swap = False,
# _cmd_bits = 8,
# _param_bits = 8,
# _init_bus = True

#fb1 = display_bus.allocate_framebuffer(BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM) #lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA)  lcd_bus.MEMORY_SPIRAM
#fb2 = display_bus.allocate_framebuffer(BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM) #lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA)  lcd_bus.MEMORY_SPIRAM

display = axs15231b.AXS15231B(
    display_bus,
    WIDTH,
    HEIGHT,
    #frame_buffer1=fb1,
    #frame_buffer2=fb2,
    backlight_pin=1,
    _cmd_bits=32,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True,
    # backlight_on_state=axs15231b.STATE_PWM, https://github.com/micropython/micropython/pull/16090
)

print('Hello LCD')
print(f"Display size: {WIDTH}x{HEIGHT}")

display.set_power(True)
display.set_backlight(100)
# PWM frequency for backlight
#display._backlight_pin.freq(2000)

display.init(1)  # use 1 type config

class TouchCal:
    def __init__(self):
        self.alphaX = None
        self.betaX = None
        self.deltaX = None
        self.alphaY = None
        self.betaY = None
        self.deltaY = None

    @staticmethod
    def save():
        pass

# I2C_NUM_0
# I2C_CLK_SPEED_HZ            400000

# PIN_NUM_QSPI_TOUCH_SCL  (GPIO_NUM_8)
# PIN_NUM_QSPI_TOUCH_SDA  (GPIO_NUM_4)



import axs15231_touch
from i2c import I2C

cal = TouchCal()

i2c_bus = I2C.Bus(host=1, sda=4, scl=8)
touch_i2c = I2C.Device(i2c_bus, axs15231_touch.I2C_ADDR, axs15231_touch.BITS)
touch = axs15231_touch.AXS15231(touch_i2c, touch_cal=cal, debug=False)

print('is_calibrate is', touch.is_calibrated)

# # LVGL TEST
# import task_handler
# th = task_handler.TaskHandler()
#
#
#
# print('Hello LVGL')
#
# scr = lv.screen_active()
# scr.set_style_bg_color(lv.color_hex(0x000000), 0)
#
#
# print('Left TOP')
# # Left TOP
# rect = lv.obj(scr)
# rect.set_size(50, 50)
# rect.set_pos(0, 0)
# rect.set_style_bg_color(lv.color_make(255, 0, 0), 0) # red
#
# print('Right TOP')
# # Right TOP
# rect = lv.obj(scr)
# rect.set_size(50, 50)
# rect.set_pos(WIDTH-50, 0)
# rect.set_style_bg_color(lv.color_make(0, 255, 0), 0) # green
#
# print('Left BOTTOM')
# # Left BOTTOM
# rect = lv.obj(scr)
# rect.set_size(50, 50)
# rect.set_pos(0, HEIGHT-50)
# rect.set_style_bg_color(lv.color_make(0, 0, 255), 0) # blue
#
# print('Right BOTTOM')
# # Right BOTTOM
# rect = lv.obj(scr)
# rect.set_size(50, 50)
# rect.set_pos(WIDTH-50, HEIGHT-50)
# rect.set_style_bg_color(lv.color_make(255, 255, 255), 0) # white
#
# # Draw cross lines from inner corners to inner corners
# line1 = lv.line(scr)
# line2 = lv.line(scr)
#
# # Define points for the lines
# points1 = [
#     {"x": 50, "y": 50},                  # Inner top-left corner
#     {"x": WIDTH - 50, "y": HEIGHT - 50}  # Inner bottom-right corner
# ]
# points2 = [
#     {"x": WIDTH - 50, "y": 50},          # Inner top-right corner
#     {"x": 50, "y": HEIGHT - 50}          # Inner bottom-left corner
# ]
#
# # Set the points for the lines
# line1.set_points(points1, 2)
# line2.set_points(points2, 2)
#
# # Set line colors (white in this case)
# line1.set_style_line_color(lv.color_make(255, 255, 255), 0)
# line2.set_style_line_color(lv.color_make(255, 255, 255), 0)
#
# # Set line width
# line1.set_style_line_width(2, 0)
# line2.set_style_line_width(2, 0)
# #
# #
# # Slider
# slider = lv.slider(scr)
# slider.set_size(200, 50)
# slider.center()
#
# label = lv.label(scr)
# label.set_text(f"{WIDTH}x{HEIGHT}")
# label.align(lv.ALIGN.CENTER, 0, -100)
# label.set_style_text_font(lv.font_montserrat_16, 0)


