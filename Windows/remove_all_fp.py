#  Import FingerprintSensor class from fingerprint module
from fingerprint import FingerprintSensor

#  Set the serial comport for the connected sensor
COM_PORT = "COM7"  # /dev/ttyS0"

#  Create class object
fp = FingerprintSensor()
#  Initialise the sensor serial with the COM port and fixed baud rate of
#  115200, set "use_thread" argument as false
fp.connect_sensor(port=COM_PORT, baud_rate=9600, use_thread=False)

#  use remove_all_fingerprints function to remove all the fingerprints
#  stored in the fingerprint sensor
fp.remove_all_fingerprints()

#  Use read_rx to wait and read the serial input,
#  print or store the sensor output
print(fp.read_rx())

#  Disconnect the serial fingerprint sensor
fp.disconnect_sensor()
