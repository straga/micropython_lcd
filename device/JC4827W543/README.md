

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

### Building firmware
If you encounter errors while compiling the firmware, \
you can use the configured [firmware](firmware)

### Flash ready firmware
```
python3 -m esptool --chip esp32s3 -p /dev/tty.usbmodem11101 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 4MB --flash_freq 80m --erase-all 0x0 device/JC4827W543/lvgl_micropy_ESP32_GENERIC_S3-SPIRAM_OCT-4.bin
```
### Possible errors.

When running a project from an IDE, such as PyCharm, you may see the error:

```
File "main.py", line 1, in <module>
File "lv_config.py", line 54, in <module>
TypeError: can't convert module to int
```

Ignore it and reboot the board using the rst button; everything should work.

After a long period of inactivity, the board may not work correctly.\
Noise appears in the display when turned on, and rebooting won't fix this.

Solution: reboot the board while holding the boot button (rst+boot). \
Then reboot the board using the rst button. \
Connecting to a computer is not necessary at this point, \
and you can power the board using a battery. \
This may help keep the finished project running until the cause of this issue is resolved in the future.