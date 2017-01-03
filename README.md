# raspi-scripts
Simple Sample / Demo / Utility Scripts for Raspberry Pi 

## python/pibrella-wiimote.py
Simple script to allow a WiiMote to connect to a Raspberry Pi and provide input to control two motors connected to a Pibrella board. The script also uses the LEDs and Button on the Pibrella to show status, and connect the Wiimote respectively. 

* Requires python-cwiid (sudo apt-get install python-cwiid)
* Requires Pibrella & Library (https://github.com/pimoroni/pibrella)

#### To Run:
`python pibrella-wiimote.py`

#### Notes:
* The LEDs show 3 states   
  Red - WiiMote not connected  
   Flashing Yellow - Attempting to connect Pi to WiiMote  
   Green - WiiMote and Pi connected  
   
   
* To initiate connection, press buttons 1 and 2 on the WiiMote together, then press the button on the Pibrella. The blue LEDs on the WiiMote should flash, and the Pibrella should flash yellow. If the two devices sync correctly, the WiiMote will show LED 1 lit, and the Pibrella will show green. If it fails, the WiiMote should show no LEDs lit, and the Pibrella should return to red.  


* To disconnect the two devices, press buttons + and - on the WiiMote together. The WiiMote should vibrate and the LED should go out, and the Pibrella should switch to red. You can then reconnect as above.


* If the WiiMote disconnects unexpectedly, the script will not handle this and the resulting behaviour is 'undefined'.


* The script has been developed and tested using a Raspberry Pi 3 (with onboard WiFi and Bluetooth) and Pibrella add-on mounted on a Pimoroni STS-PI chassis, with the right motor connected to output 'e' and the left to output 'f'. I used a fresh, full install of the lastest Raspbian, update to the latest levels. As such, the Bluetooth stuff just worked, with nothing else required.


* This script was based on the Raspberry Pi Spy post here:  
http://www.raspberrypi-spy.co.uk/2013/02/nintendo-wii-remote-python-and-the-raspberry-pi/