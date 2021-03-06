from oled_091 import SSD1306
from os import path
from time import sleep

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = path.join(DIR_PATH, "Fonts/GothamLight.ttf")

display = SSD1306()

#  Import FingerprintSensor class from fingerprint module
from fingerprint import FingerprintSensor

#  Set the serial comport for the connected sensor
COM_PORT = "/dev/ttyS0"  # 

#  Create class object
fp = FingerprintSensor()
display = SSD1306()
#  Initialise the sensor serial with the COM port and fixed baud rate of
#  115200, set "use_thread" argument as false
fp.connect_sensor(port=COM_PORT, baud_rate=9600, use_thread=False)

#  Use unlock_with_fingerprint function of FingerprintSensor to send
#  fingerprint unlock command to the sensor
fp.unlock_with_fingerprint()

display.DirImage(path.join(DIR_PATH, "Images/SB.png"))
display.DrawRect()
display.ShowImage()
sleep(1)
display.PrintText("Place your Finger", FontSize=14)
display.ShowImage()

#  Wait for the sensor to compare and send the success message
while True:
    rec = fp.read_rx()
    if rec:
        print(rec)
        #  If the sensor sends "Matched" string exit the loop
        if "Matched!" in rec:
            display.PrintText(rec, cords=(2, 2), FontSize=14)
            display.ShowImage()
            break
        else:
            display.PrintText(rec, cords=(2, 2), FontSize=14)
            display.ShowImage()

#  Disconnect the serial fingerprint sensor
fp.disconnect_sensor()
