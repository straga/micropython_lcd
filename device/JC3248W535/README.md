

## Features
- ESP32-S3 3.5-inch capacitive touch IPS module 8M PSRAM 16M 320*480
- Compatible with MicroPython
- Model: JC3248W535
- LCD: axs15231b QSPI
- TOUCH: axs15231b I2C

## Pin info

```
## Panel

# LCD_QSPI_HOST           (SPI2_HOST)     SPI2_HOST=1,  ok

# PIN_NUM_QSPI_CS         (GPIO_NUM_45)                 ok
# PIN_NUM_QSPI_PCLK       (GPIO_NUM_47)                 ok

# PIN_NUM_QSPI_DATA0      (GPIO_NUM_21)                 ok
# PIN_NUM_QSPI_DATA1      (GPIO_NUM_48)                 ok
# PIN_NUM_QSPI_DATA2      (GPIO_NUM_40)                 ok
# PIN_NUM_QSPI_DATA3      (GPIO_NUM_39)                 ok

# PIN_NUM_QSPI_RST        (GPIO_NUM_NC)                 NC
# PIN_NUM_QSPI_DC         (GPIO_NUM_8)                  ok
# PIN_NUM_QSPI_TE         (GPIO_NUM_38)
# PIN_NUM_QSPI_BL         (GPIO_NUM_1)                  ok

## Touch

# I2C_NUM                     (I2C_NUM_0)               ok
# I2C_CLK_SPEED_HZ            400000                    ok

# PIN_NUM_QSPI_TOUCH_SCL  (GPIO_NUM_8)                  ok
# PIN_NUM_QSPI_TOUCH_SDA  (GPIO_NUM_4)                  ok
# PIN_NUM_QSPI_TOUCH_RST  (-1)
# PIN_NUM_QSPI_TOUCH_INT  (-1)

```
## Driver
- https://github.com/straga/micropython_lcd/tree/master/device/JC3248W535/driver/axs15231b

## Firmware
- For upload: https://github.com/straga/micropython_lcd/tree/master/device/JC3248W535/firmware

## Board for Micropython
- https://github.com/straga/micropython_lcd/tree/master/device/JC3248W535/board

## Info


- For build Firmware with lvgl: https://github.com/lvgl-micropython/lvgl_micropython/
- Driver progress: https://github.com/lvgl-micropython/lvgl_micropython/discussions/161



### esp-idf 5.2.2 - micropython 1.24 ~ 1.25prevew(with pwm fix - 31.10.2024)


## Firmware
### erase
```
python -m esptool -p COM16 -b 460800 --before default_reset --after hard_reset --chip auto  erase_flash
```

### flash
```
python -m esptool -p COM16 --chip esp32s3 -b 460800 --before default_reset --after no_reset write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m 0x0 bootloader.bin 0x10000 partition-table.bin 0x15000 ota_data_initial.bin 0x20000 micropython.bin
```

## Upload files and drive

```
import network
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect("SSID", "KEY")
```

```
import webrepl
webrepl.start(password="micro")
```
or

```
import uftpd
```

## Test

```
import test
```