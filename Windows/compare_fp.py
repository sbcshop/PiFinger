#  Import FingerprintSensor class from fingerprint module
from fingerprint import FingerprintSensor

#  Set the serial comport for the connected sensor
COM_PORT = "COM7"  # /dev/ttyS0"

#  Create class object
fp = FingerprintSensor()
#  Initialise the sensor serial with the COM port and fixed baud rate of
#  115200, set "use_thread" argument as false
fp.connect_sensor(port=COM_PORT, baud_rate=9600, use_thread=False)

#  Use unlock_with_fingerprint function of FingerprintSensor to send
#  fingerprint unlock command to the sensor
fp.unlock_with_fingerprint()

#  Wait for the sensor to compare and send the success message
while True:
    rec = fp.read_rx()
    if rec:
        print(rec)
        #  If the sensor sends "Matched" string exit the loop
        if "Matched!" in rec:
            break

#  Disconnect the serial fingerprint sensor
fp.disconnect_sensor()
