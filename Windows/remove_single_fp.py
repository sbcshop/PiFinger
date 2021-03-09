#  Import FingerprintSensor class from fingerprint module
from fingerprint import FingerprintSensor

#  Set the serial comport for the connected sensor
COM_PORT = "COM7"  # /dev/ttyS0"

#  Create class object
fp = FingerprintSensor()
#  Initialise the sensor serial with the COM port and fixed baud rate of
#  115200, set "use_thread" argument as false
fp.connect_sensor(port=COM_PORT, baud_rate=9600, use_thread=False)

#  Use the remove_one_fingerprint function of FingerprintSensor class,
#  and pass the id of the fingerprint you want to remove as the argument
fp.remove_one_fingerprint(fp_id=1)

#  Print the sensor output, to check the success or failure of the command
print(fp.read_rx())

#  Disconnect the serial fingerprint sensor
fp.disconnect_sensor()
