#  Import FingerprintSensor class from fingerprint module
from fingerprint import FingerprintSensor

#  Set the serial comport for the connected sensor
COM_PORT = "COM7"  # /dev/ttyS0"

#  Create class object
fp = FingerprintSensor()
#  Initialise the sensor serial with the COM port and fixed baud rate of
#  115200, set "use_thread" argument as false
fp.connect_sensor(port=COM_PORT, baud_rate=9600, use_thread=False)

#  Use get_device_status function of FingerprintSensor to send the command
#  to sensor, the sensor will respond with the device state.
fp.get_device_status()
# print the device state
print(fp.read_rx())

#  Disconnect the serial fingerprint sensor
fp.disconnect_sensor()
