# PiFinger
PiFinger, the first-ever Fingerprint HAT for Raspberry Pi Comprise of onboard Nuvoton MCU with an on-chip crypto-accelerator, Cortex-M23 TrustZone, and XOM facilities. A user can use the communication protocol to the PiFinger with commands over the UART protocol with the Baud rate 115200 bps or USB 2.0 full speed.

### Enable I2C and Serial Interface for Raspberry Pi

 Open a terminal and run the following commands to enable I2C and Serial：


* ``` sudo raspi-config ```

Choose Interfacing Options -> I2C ->yes 

<img src="Images/en_i2c_all.png" />


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

#### GUI Features 

1) Compare Fingerprint - Option to Compare registered Fingerprint.

2) Add Fingerprint - Add New Fingerprint, will assign an ID for each successful registration.

3) Remove Fingerprint ( By ID) - Remove registered Fingerprint for a specific ID.

4) Remove All Fingerprint (Registered) - Remove all fingeprint in a single click.
