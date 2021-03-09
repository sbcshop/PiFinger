
from serial_comm import SerialComm

DEVICE_STATUS_STRING = b'<C>GetDS</C>'
SENSOR_INFO_STRING = b'<C>FpImageInformation</C>'
NUM_FINGERPRINT_STRING = b'<C>CheckRegisteredNo</C>'
FW_VER_STRING = b'<C>GetFWVer</C>'
FINGERPRINT_UNLOCK_STRING = b'<C>UnlockCompareFp</C>'
REGISTER_FINGERPRINT_STRING = b'<C>RegisterFingerprint</C>'
REGISTER_FINGERPRINT_AT_STRING = "<C>RegisterOneFp={}</C>"
COMPARE_FINGERPRINT_STRING = b'<C>CompareFingerprint</C>'
SCAN_IMAGE_STRING = b'<C>ScanFpImage</C>'
SET_PASSWORD_STRING = b'<C>SetPWD=</C>'
CLEAR_PASSWORD_STRING = b'<C>ClearPWD</C>'
CLEAR_FINGERPRINT_STRING = b'<C>ClearRegisteredFp</C>'
CLEAR_FINGERPRINT_AT_STRING = "<C>ClearOneFp={}</C>"
CLEAR_FP_AT_STRING = b"<C>ClearOneFp=1<C>"
LOCK_DEVICE_STRING = b'<C>LockDevice</C>'
SET_BAUD_9600_STRING = b'<C>Baudrate=9600</C>'
SET_BAUD_115200_STRING = b'<C>Baudrate=115200</C>'
SET_ACTIVE_MODE_STRING = b"<C>SetActiveMode</C>"
SET_ACTIVE_DEMO_MODE_STRING = b"<C>SetActiveMode=0</C>"
SET_ACTIVE_OPERATION_MODE_STRING = b"<C>SetActiveMode=1</C>"


class FingerprintSensor(SerialComm):
    def __init__(self):
        super().__init__()

    def connect_sensor(self, port='/dev/ttyS0', baud_rate=96200,
                       use_thread=True):
        return self.connect_port(port=port, baud_rate=baud_rate,
                                 timeout=0.5, use_thread=use_thread)

    def disconnect_sensor(self):
        self.disconnect()

    def get_device_status(self):
        return self.send_cmd(DEVICE_STATUS_STRING)

    def sensor_image_info(self):
        return self.send_cmd(SENSOR_INFO_STRING)

    def get_fp_numbers(self):
        return self.send_cmd(NUM_FINGERPRINT_STRING)

    def get_firmware_version(self):
        return self.send_cmd(FW_VER_STRING)

    def unlock_with_fingerprint(self):
        return self.send_cmd(FINGERPRINT_UNLOCK_STRING)

    def register_fingerprint(self):
        return self.send_cmd(REGISTER_FINGERPRINT_STRING)

    def register_fingerprint_at(self, num):
        send_string = REGISTER_FINGERPRINT_AT_STRING.format(num)
        send_string = send_string.encode("utf-8")
        return self.send_cmd(send_string)

    def remove_all_fingerprints(self):
        self.send_cmd(CLEAR_FINGERPRINT_STRING)

    def remove_one_fingerprint(self, fp_id):
        self.send_cmd(CLEAR_FINGERPRINT_AT_STRING.format(fp_id).encode(
            "utf-8"))

    def compare_fingerprint(self):
        return self.send_cmd(COMPARE_FINGERPRINT_STRING)

    def set_active_mode(self):
        return self.send_cmd(SET_ACTIVE_DEMO_MODE_STRING)

    def read_fp_image(self):
        return self.send_cmd(SCAN_IMAGE_STRING)

    def send_cmd(self, command):
        if self._connected:
            self.flush_input()
            return self.write(command)

    def read_rx(self):
        # while not self._waiting:  # Wait for RX data comes
        #     pass
        rx_str = ""
        while True:
            rx_byte = self.read_line()
            if rx_byte == b"":
                break
            rx_str += rx_byte.decode("utf-8")

        return rx_str


if __name__ == "__main__":
    from time import sleep

    fp = FingerprintSensor()

    fp.connect_sensor(port="COM7")
    sleep(1)
    # print(fp.get_device_status())
    # print(fp.sensor_image_info())
    # print(fp.get_firmware_version())
    #
    # print(fp.get_fp_numbers())

    print(fp.compare_fingerprint())
    # print(fp.read_fp_image())
    # while True:
    #     dat = fp.read_rx()
    #     if dat:
    #         print(dat)
    #         if "Mismatch" in dat:
    #             print(fp.compare_fingerprint())
    #         elif "Matched!" in dat:
    #             break

    fp.disconnect_sensor()
