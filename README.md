# PiFinger
Biometric HAT for Raspberry Pi

### Enable I2C and Serial Interface

 Open a terminal and run the following commands to enable Serial on Raspberry Pi：

* ``` sudo raspi-config ```

Choose Interfacing Options -> Serial -> No -> Yes

<img src="Images/en_serial_full.png" />

## Testing

### Clone Repository

``` git clone https://github.com/sbcshop/PiFinger.git ```

``` cd PiFinger ```

``` cd Raspberry_Pi ```

Run GUI by running below command:

``` python3 PiFinger_GUI.py ```

Select <b>COM port</b> and Baud Rate ( default is 115200) from above GUI ("/dev/ttyS0" in case of default connection), 
and click on connect button to start communication with fingerprint sensor.

#### Features 

1) Compare Fingerprint -

2) Add Fingerprint -

3) Remove Fingerprint ( By ID) -

4) Remove All Fingerprint (Registered) -
