

## Features
- ESP32-S3 3.5-inch capacitive touch IPS module 8M PSRAM 16M 320*480
- Compatible with MicroPython
- Model: JC3248W535
- LCD: axs15231b QSPI
- TOUCH: axs15231b I2C


### firmware source
https://github.com/straga/lvgl_micropython/tree/feature/spi_bus_fast

### Build
```
with my frozen
python3 make.py esp32 BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT --flash-size=16 DISPLAY=axs15231b INDEV=axs15231 --skip-partition-resize --partition-size=4194304 --ota FROZEN_MANIFEST='/my/manifest.py'

just build
python3 make.py esp32 BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT --flash-size=16 DISPLAY=axs15231b INDEV=axs15231 --skip-partition-resize --partition-size=4194304 --ota
```

### Flash
```
python3 -m esptool --chip esp32s3 -p /dev/tty.usbmodem11101 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 16MB --flash_freq 80m --erase-all 0x0 lvgl_micropython/build/lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-16.bin
```

### Upload
copy file nv3041aG.py from JC4827W543 
Files for drivers and test.
