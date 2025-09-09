# Based on the work by straga (https://github.com/straga)
# https://github.com/straga/micropython_lcd/blob/master/device/JC3248W535/driver/axs15231b/_axs15231b_init_type1.py
# Copyright (c) 2024 - 2025 Kevin G. Schlosser

import time
from micropython import const  # NOQA
import lvgl as lv  # NOQA


AXS_LCD_NOP      = 0x00  # No operation (C)
AXS_LCD_SWRESET  = 0x01  # Software reset (C)
AXS_LCD_RDDID    = 0x04  # Read display (R)
AXS_LCD_RDNUMED  = 0x05  # Read Number of the Errors on DSI (R)
AXS_LCD_RDDST    = 0x09  # Read display status (R)
AXS_LCD_RDDPM    = 0x0A  # Read display power (R)
AXS_LCD_RDDMADC  = 0x0B  # Read memory data access control (R)
AXS_LCD_RDDIPF   = 0x0C  # Read Interface Pixel Format (R)
AXS_LCD_RDDIM    = 0x0D  # Read display image (R)
AXS_LCD_RDDSM    = 0x0E  # Read display signal (R)
AXS_LCD_RDDSDR   = 0x0F  # Read display self-diagnostic result (R)
AXS_LCD_SLPIN    = 0x10  # Sleep in (C)
AXS_LCD_SLPOUT   = 0x11  # Sleep out (C)
AXS_LCD_PTLON    = 0x12  # Partial mode on (C)
AXS_LCD_NORON    = 0x13  # Partial mode off(Normal) (C)
AXS_LCD_INVOFF   = 0x20  # Display inversion off (C)
AXS_LCD_INVON    = 0x21  # Display inversion on (C)
AXS_LCD_ALLPOFF  = 0x22  # All pixel off (C)
AXS_LCD_ALLPON   = 0x23  # All pixel on (C)
AXS_LCD_ALLPFILL = 0x24  # All pixel fill given color (W)
AXS_LCD_GAMSET   = 0x26  # Gamma curve set (W)
AXS_LCD_DISPOFF  = 0x28  # Display off (C)
AXS_LCD_DISPON   = 0x29  # Display on (C)
AXS_LCD_CASET    = 0x2A  # Column address set (W)
AXS_LCD_RASET    = 0x2B  # Row address set (W)
AXS_LCD_RAMWR    = 0x2C  # Memory write any length MIPI/SPI/QSPI/DBI (W)
AXS_LCD_RAMRD    = 0x2E  # Memory read any length SPI/QSPI/DBI (R)
AXS_LCD_RAWFILL  = 0x2F  # Memory fill given color at window (W)
AXS_LCD_PTLAR    = 0x30  # Partial start/end address set (W)
AXS_LCD_PTLARC   = 0x31  # set_partial_columns (W)
AXS_LCD_VSCRDEF  = 0x33  # Vertical scrolling definition (W)
AXS_LCD_TEOFF    = 0x34  # Tearing effect line off (C)
AXS_LCD_TEON     = 0x35  # Tearing effect line on (W)
AXS_LCD_MADCTL   = 0x36  # Memory data access control (W)
AXS_LCD_VSCRSADD = 0x37  # Vertical scrolling start address (W)
AXS_LCD_IDMOFF   = 0x38  # Idle mode off (C)
AXS_LCD_IDMON    = 0x39  # Idle mode on (C)
AXS_LCD_IPF      = 0x3A  # Interface pixel format (W)
AXS_LCD_RAMWRC   = 0x3C  # Memory write continue any length MIPI/SPI/QSPI/DBI (W)
AXS_LCD_RAMRDC   = 0x3E  # Memory read continue any length SPI/QSPI/DBI (R)
AXS_LCD_TESCAN   = 0x44  # Set tear scanline (W)
AXS_LCD_RDTESCAN = 0x45  # Get tear scanline (R)
AXS_LCD_WRDISBV  = 0x51  # Write display brightness value (W)
AXS_LCD_RDDISBV  = 0x52  # Read display brightness value (R)
AXS_LCD_WRCTRLD  = 0x53  # Write CTRL display (W)
AXS_LCD_RDCTRLD  = 0x54  # Read CTRL dsiplay (R)
AXS_LCD_RDFCHKSU = 0xAA  # Read First Checksum (R)
AXS_LCD_RDCCHKSU = 0xAA  # Read Continue Checksum (R)
AXS_LCD_RDID1    = 0xDA  # Read ID1 (R)
AXS_LCD_RDID2    = 0xDB  # Read ID2 (R)
AXS_LCD_RDID3    = 0xDC  # Read ID3 (R)
AXS_LCD_DSTB     = 0x90  # Enter Deep-Standby (W)


def init(self):
    param_buf = bytearray(15)
    param_mv = memoryview(param_buf)


    # Color and Orientation
    param_buf[0] = (
        self._madctl(
            self._color_byte_order,
            self._ORIENTATION_TABLE  # NOQA
        )
    )
    self.set_params(AXS_LCD_MADCTL, param_mv[:1])

    # Pixel size
    color_size = lv.color_format_get_size(self._color_space)
    if color_size == 2:
        pixel_format = 0x55
    else:
        pixel_format = 0x66

    param_buf[0] = pixel_format
    self.set_params(AXS_LCD_IPF, param_mv[:1])

    # # Disable Partial Display Mode (return to Normal Display Mode)
    self.set_params(AXS_LCD_NORON)
    time.sleep_ms(10)

    #  AXS_LCD_SLPOUT
    self.set_params(AXS_LCD_SLPOUT)
    time.sleep_ms(150)

    #  AXS_LCD_DISPON
    self.set_params(AXS_LCD_DISPON)
    time.sleep_ms(150)

    # All Pixels off
    param_buf[:1] = bytearray([0x00])
    self.set_params(0x22, param_mv[:1])
    time.sleep_ms(200)
