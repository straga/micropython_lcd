

 ## Features
- ESP32-S3 4.3-inch capacitive touch IPS module 8M PSRAM 4M 480*270
- Compatible with MicroPython
- Model: JC4827W543
- LCD: NV3041A QSPI
- TOUCH: GT911 I2C

### Build
```
python3 make.py esp32 BOARD=ESP32_GENERIC_S3 BOARD_VARIANT=SPIRAM_OCT --flash-size=4 DISPLAY=nv3041a INDEV=gt911
```

### Flash
```
python3 -m esptool --chip esp32s3 -p /dev/tty.usbmodem11101 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 4MB --flash_freq 80m --erase-all 0x0 lvgl_micropython/build/lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-4.bin
```

### Upload

Files for drivers and test.

