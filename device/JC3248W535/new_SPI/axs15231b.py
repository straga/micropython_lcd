# AXS15231B Driver with SPIBusFast for Partial Updates Optimization
# Based on the original AXS15231B driver by straga and Kevin G. Schlosser


import display_driver_framework
from micropython import const
import time

import lcd_bus
import lvgl as lv

STATE_HIGH = display_driver_framework.STATE_HIGH
STATE_LOW = display_driver_framework.STATE_LOW
STATE_PWM = display_driver_framework.STATE_PWM

BYTE_ORDER_RGB = display_driver_framework.BYTE_ORDER_RGB
BYTE_ORDER_BGR = display_driver_framework.BYTE_ORDER_BGR

_RASET = const(0x2B)
_CASET = const(0x2A)
_MADCTL = const(0x36)

_RAMWR = const(0x2C)
_RAMWRC = const(0x3C)

# QSPI command mode constants for AXS15231B controller
# These are used to construct 32-bit QSPI commands in format:
# [MODE:8][COMMAND:8][DUMMY:8][DATA:8]
_WRITE_CMD = const(0x02)    # Command mode for parameter writes
_WRITE_COLOR = const(0x32)  # Color mode for pixel data writes

# MADCTL (Memory Data Access Control) register bits for screen orientation
# These control how the display controller maps logical coordinates to physical pixels
_MADCTL_MH = const(0x04)  # Horizontal refresh direction: 0=Left to Right, 1=Right to Left
_MADCTL_BGR = const(0x08) # Color order: 0=RGB, 1=BGR
_MADCTL_ML = const(0x10)  # Vertical refresh direction: 0=Top to Bottom, 1=Bottom to Top

_MADCTL_MV = const(0x20)  # Row/Column exchange: 0=Normal, 1=Swap X/Y (for rotation)
_MADCTL_MX = const(0x40)  # Column address order: 0=Left to Right, 1=Right to Left  
_MADCTL_MY = const(0x80)  # Row address order: 0=Top to Bottom, 1=Bottom to Top

_WRDISBV = const(0x51)
_SW_RESET = const(0x01)


class AXS15231B(display_driver_framework.DisplayDriver):
    """
    AXS15231B driver with partial updates optimization via SPIBusFast.
    
    Key differences from standard driver:
    - Uses lcd_bus.SPIBusFast instead of lcd_bus.SPIBus
    - SPIBusFast accumulates partial updates into full frame buffer
    - RGB565 byte swap performed only for dirty areas (optimization from PR #609)
    - Data sent in 10KB chunks when LVGL signals last_update=True
    
    This driver is specifically optimized for QSPI displays with partial update support.
    For maximum performance, use with SPIBusFast bus which provides:
    - Double buffering with RTOS task
    - Partial update accumulation
    - Chunked QSPI transmission
    - Hardware rotation support
    """
    # Orientation table for MADCTL register values
    # Each entry corresponds to 0°, 90°, 180°, 270° rotations
    _ORIENTATION_TABLE = (
        0,                                      # 0°:   Normal orientation
        _MADCTL_MV,                            # 90°:  Row/column exchange 
        _MADCTL_MX | _MADCTL_MY,              # 180°: Flip both X and Y
        _MADCTL_MV | _MADCTL_MX | _MADCTL_MY  # 270°: Row/column exchange + flip both
    )


    def __init__(
        self,
        data_bus,
        display_width,
        display_height,
        frame_buffer1=None,
        frame_buffer2=None,
        reset_pin=None,
        reset_state=STATE_HIGH,
        power_pin=None,
        power_on_state=STATE_HIGH,
        backlight_pin=None,
        backlight_on_state=STATE_HIGH,
        offset_x=0,
        offset_y=0,
        color_byte_order=BYTE_ORDER_RGB,
        color_space=lv.COLOR_FORMAT.RGB888,
        rgb565_byte_swap=False
    ):
        num_lanes = data_bus.get_lane_count()

        # Check if SPIBusFast is used for QSPI - this enables partial updates optimization
        if isinstance(data_bus, lcd_bus.SPIBusFast) and num_lanes == 4:
            print(f"AXS15231B: Using SPIBusFast with {num_lanes} lanes - PARTIAL UPDATES ENABLED")
            self.__qspi = True
            _cmd_bits = 32  # QSPI command format: [MODE][ADDR][DUMMY][DATA]
        elif isinstance(data_bus, lcd_bus.SPIBus) and num_lanes == 4:
            # Warning if regular SPIBus is used - partial updates won't work
            print("AXS15231B: WARNING - Using regular SPIBus. Consider SPIBusFast for optimization")
            self.__qspi = True
            _cmd_bits = 32
        else:
            if isinstance(data_bus, lcd_bus.I80Bus) and num_lanes > 8:
                raise RuntimeError('Only 8 lanes is supported when using the I80Bus')

            self.__qspi = False
            _cmd_bits = 8

        if not isinstance(data_bus, (lcd_bus.RGBBus, lcd_bus.I80Bus, lcd_bus.SPIBus, lcd_bus.SPIBusFast)):
            raise RuntimeError('incompatable bus driver')

        self._brightness = 0xD0

        super().__init__(
            data_bus,
            display_width,
            display_height,
            frame_buffer1,
            frame_buffer2,
            reset_pin,
            reset_state,
            power_pin,
            power_on_state,
            backlight_pin,
            backlight_on_state,
            offset_x,
            offset_y,
            color_byte_order,
            color_space,
            rgb565_byte_swap,
            _cmd_bits=_cmd_bits,
            _param_bits=8,
            _init_bus=True
        )
        
        # Log which bus type is being used for diagnostics
        if isinstance(data_bus, lcd_bus.SPIBusFast):
            print(f"AXS15231B_Fast: Using SPIBusFast with {display_width}x{display_height} partial updates optimization")
        else:
            print(f"AXS15231B_Fast: Using regular bus without partial updates optimization")

    def reset(self):
        """
        Reset the AXS15231B display controller.
        
        Uses either hardware reset (via reset pin) or software reset command.
        Hardware reset is preferred when available as it's more reliable.
        """
        if self._reset_pin is None:
            # Software reset via command
            self.set_params(_SW_RESET)
        else:
            # Hardware reset sequence
            self._reset_pin.value(not self._reset_state)  # Assert reset
            time.sleep_ms(10)  # Hold reset low
            self._reset_pin.value(self._reset_state)      # Release reset
            time.sleep_ms(10)  # Wait for reset to take effect
            self._reset_pin.value(not self._reset_state)  # Final state
        time.sleep_ms(120)  # Wait for controller to be ready

    def init(self, type=None):  # NOQA
        """
        Initialize the display controller.
        
        For QSPI/SPI buses, calls parent initialization which sends
        the initialization sequence. For RGB buses, just marks as initialized.
        """
        if not isinstance(self._data_bus, lcd_bus.RGBBus):
            # Initialize via SPI/QSPI with command sequence
            super().init(type)
        else:
            # RGB bus doesn't need command initialization
            self._initilized = True

    def set_brightness(self, value):
        """
        Set display backlight brightness.
        
        Args:
            value (float): Brightness percentage (0-100)
        """
        # Convert percentage to 8-bit value (0-255)
        value = int(value / 100.0 * 255)
        value = max(0x00, min(value, 0xFF))  # Clamp to valid range

        self._brightness = value

        # Send brightness command to controller
        self._param_buf[0] = value
        self.set_params(_WRDISBV, self._param_mv[:1])

    def get_brightness(self):
        """
        Get current display brightness.
        
        Returns:
            float: Brightness percentage (0-100)
        """
        return round(self._brightness / 255.0 * 100.0, 1)

    def set_params(self, cmd, params=None):
        """Send command with parameters to display controller."""
        if self.__qspi:
            # Convert 8-bit command to 32-bit QSPI format:
            # [WRITE_CMD:8][COMMAND:8][0:8][0:8] = 0x02nnnn00
            cmd &= 0xFF           # Ensure command is 8-bit
            cmd <<= 8             # Shift to bits 15:8
            cmd |= _WRITE_CMD << 24  # Add mode bits 31:24

        self._data_bus.tx_param(cmd, params)

    def _set_memory_location(self, x1: int, y1: int, x2: int, y2: int):
        """
        Set memory write window coordinates.
        
        For SPIBusFast optimization, we don't need to set window coordinates here
        because SPIBusFast handles full frame buffer updates internally.
        LVGL calls this for each partial update, but SPIBusFast accumulates
        all updates and sends the complete frame when last_update=True.
        
        Returns _RAMWR command for compatibility with display framework.
        """
        return _RAMWR




