
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