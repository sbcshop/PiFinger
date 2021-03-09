#  Import FingerprintSensor class from fingerprint module
from fingerprint import FingerprintSensor

#  Set the serial comport for the connected sensor
COM_PORT = "COM15"  # /dev/ttyS0"

#  Create class object
fp = FingerprintSensor()
#  Initialise the sensor serial with the COM port and fixed baud rate of
#  115200, set "use_thread" argument as false
fp.connect_sensor(port=COM_PORT, baud_rate=9600, use_thread=False)

#  Use register_fingerprint function of FingerprintSensor to send
#  fingerprint registration command to the sensor
fp.register_fingerprint()

#  Read the sensor output, as the sensor will guide through 3 step
#  registration process
while True:
    #  Read the sensor output, if it's not null print the received data and
    #  follow the steps printed on the console
    rec = fp.read_rx()
    if rec:
        print(rec)

#  Disconnect the serial fingerprint sensor
fp.disconnect_sensor()
