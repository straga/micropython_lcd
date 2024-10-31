from micropython import const
import ustruct
import pointer_framework

# Constants
AXS_MAX_TOUCH_NUMBER = const(1)
AXS_TOUCH_POINT_NUM = const(1)
I2C_ADDR = const(0x3B)
BITS = 8

class TouchRecord:
    def __init__(self):
        self.gesture = 0
        self.num = 0
        self.x = 0
        self.y = 0
        self.event = 0

class AXS15231(pointer_framework.PointerDriver):
    def __init__(self, device, touch_cal=None,
                 startup_rotation=pointer_framework.lv.DISPLAY_ROTATION._0,
                 debug=False):

        self._device = device
        super().__init__(
            touch_cal=touch_cal, startup_rotation=startup_rotation, debug=debug
        )
        self.scan_i2c()

    def scan_i2c(self):
        print("Scanning I2C bus...")
        devices = self._device._bus.scan()
        if devices:
            for device in devices:
                print(f"I2C device found at address: 0x{device:02X}")
        else:
            print("No I2C devices found")

    def _read_data(self):
        read_cmd = b'\xb5\xab\xa5\x5a\x00\x00' + \
                   ustruct.pack('>H', AXS_MAX_TOUCH_NUMBER * 6 + 2) + \
                   b'\x00\x00\x00'

        self._device.write(read_cmd)

        data = bytearray(AXS_MAX_TOUCH_NUMBER * 6 + 2)
        self._device.read(buf=data)

        touch_points = []
        num_points = data[AXS_TOUCH_POINT_NUM]

        if num_points and num_points <= AXS_MAX_TOUCH_NUMBER:
            for i in range(num_points):
                offset = i * 6
                record = TouchRecord()
                record.gesture = data[offset]
                record.num = data[offset + 1]
                record.x = ((data[offset + 2] & 0x0F) << 8) | data[offset + 3]
                record.y = ((data[offset + 4] & 0x0F) << 8) | data[offset + 5]
                record.event = (data[offset + 2] >> 6) & 0x03
                touch_points.append(record)

        return touch_points

    def _get_coords(self):
        touch_data = self._read_data()

        if touch_data:
            #print(f"Touch guesture: {touch_data[0].gesture}, num: {touch_data[0].num}, event: {touch_data[0].event}")
            x = touch_data[0].x
            y = touch_data[0].y

            if touch_data[0].event == 1:
                return self.RELEASED, x, y

            return self.PRESSED, x, y
        else:
            return None
