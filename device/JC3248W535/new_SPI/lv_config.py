
"""
LVGL Configuration for JC3248W535EN Display
===========================================

Display: JC3248W535EN with AXS15231B controller
Resolution: 320x480 pixels
Interface: QSPI (4-wire SPI)
Touch: AXS15231 capacitive touch controller

Hardware connections:
- Display: QSPI interface on ESP32-S3
- Touch: I2C interface
"""

from micropython import const
import machine
import lcd_bus
import lvgl as lv

# =============================================================================
# Display Configuration
# =============================================================================

# Display dimensions
WIDTH = const(320)
HEIGHT = const(480)
_BUFFER_SIZE = WIDTH * HEIGHT * 2  # RGB565 = 2 bytes per pixel

# QSPI Display Pins (JC3248W535EN)
_SCLK_PIN = const(47)    # QSPI Clock
_DATA0_PIN = const(21)   # QSPI Data 0 (MOSI equivalent)
_DATA1_PIN = const(48)   # QSPI Data 1 (MISO equivalent)
_DATA2_PIN = const(40)   # QSPI Data 2
_DATA3_PIN = const(39)   # QSPI Data 3
_CS_PIN = const(45)      # Chip Select
_DC_PIN = const(8)       # Data/Command
_BACKLIGHT_PIN = const(1)  # Backlight PWM
_RESET_PIN = None        # Reset (not connected)

# Display timing
_FREQ = const(40000000)  # 40 MHz QSPI frequency

# =============================================================================
# Touch Configuration  
# =============================================================================

# I2C Touch Pins (AXS15231 capacitive touch)
_TOUCH_SDA_PIN = const(4)    # I2C Data
_TOUCH_SCL_PIN = const(8)    # I2C Clock

# =============================================================================
# Hardware Initialization
# =============================================================================

# Initialize QSPI bus for display
spi_bus = machine.SPI.Bus(
    host=1,  # SPI2_HOST
    sck=_SCLK_PIN,
    quad_pins=(_DATA0_PIN, _DATA1_PIN, _DATA2_PIN, _DATA3_PIN)
)

# Create display bus interface
display_bus = lcd_bus.SPIBusFast(
    spi_bus=spi_bus,
    dc=_DC_PIN,
    cs=_CS_PIN, 
    freq=_FREQ,
    spi_mode=3,      # SPI mode 3 (CPOL=1, CPHA=1)
    quad=True        # Enable QSPI mode (4-wire)
)

# Allocate frame buffers in SPIRAM for better performance
#fb1 = display_bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)
#fb2 = display_bus.allocate_framebuffer(_BUFFER_SIZE, lcd_bus.MEMORY_SPIRAM)

# =============================================================================
# Display Driver Setup
# =============================================================================

import axs15231b

display = axs15231b.AXS15231B(
    display_bus,
    WIDTH,
    HEIGHT,
    #frame_buffer1=fb1,
    #frame_buffer2=fb2,
    backlight_pin=_BACKLIGHT_PIN,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True,           # Required for this display
    backlight_on_state=axs15231b.STATE_PWM
)

# Initialize display
print(f"Initializing {WIDTH}x{HEIGHT} QSPI display...")
display.set_power(True)
display.set_backlight(80)  # 80% brightness
display.init()
print("Display initialized successfully!")

# =============================================================================
# Touch Controller Setup
# =============================================================================

class TouchCal:
    """Touch calibration data placeholder"""
    def __init__(self):
        # Calibration parameters (not needed for this touch controller)
        self.alphaX = None
        self.betaX = None  
        self.deltaX = None
        self.alphaY = None
        self.betaY = None
        self.deltaY = None
        self.mirrorX = False
        self.mirrorY = False

    @staticmethod
    def save():
        """Save calibration data (placeholder)"""
        pass

# Initialize I2C bus for touch controller
import device.JC3248W535.default_SPI.axs15231 as axs15231
from i2c import I2C

i2c_bus = I2C.Bus(host=1, sda=_TOUCH_SDA_PIN, scl=_TOUCH_SCL_PIN)
touch_i2c = I2C.Device(i2c_bus, axs15231.I2C_ADDR, axs15231.BITS)

# Create touch input device
cal = TouchCal()
touch = axs15231.AXS15231(touch_i2c, touch_cal=cal, debug=False)

# Initialize touch controller
indev = axs15231.AXS15231(touch_i2c, debug=False)
indev.enable_input_priority()

print(f"Touch controller calibrated: {indev.is_calibrated}")
print("System ready!")

# =============================================================================
# Usage Notes
# =============================================================================
"""
After importing this module, you can use:

- display: AXS15231B display driver instance
- touch: AXS15231 touch controller instance  
- WIDTH, HEIGHT: Display dimensions

Example:
    import lv_config
    
    # Display is automatically initialized
    # Create LVGL objects and use normally
    
    label = lv.label(lv.screen_active())
    label.set_text("Hello World!")
    label.center()
"""
