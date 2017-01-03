#
# pibrella-wiimote.py
#
# Use a Wiimote to control LEDs and drive motors via a Pibrella for Raspberry Pi
# 
# In this example, the right side motor is connected to output e, and the left to output f
# Currently the script allows explicit connection and disconnection of the Wiimote, but unexpected
# disconnection might leave things in a strange state.

import cwiid
import pibrella
import time

# This method is called when the button on the Pibrella is pressed
def handleConnectBtnPress(pin):    
    global attemptingConnection
    global wiimote
    
    # Only attempt to connect if we aren't already connected, and not trying to connect
    if (wiimote == None and attemptingConnection == False):
    
        attemptingConnection = True
        pibrella.light.green.off()
        pibrella.light.red.off()
        pibrella.light.yellow.pulse(0, 0, 1, 1)
        try:
            wiimote=cwiid.Wiimote()
            wiimote.rpt_mode = cwiid.RPT_BTN            
            pibrella.light.green.on()
            pibrella.light.yellow.off()
            wiimote.led = 1
        except RuntimeError:
            pibrella.light.red.on()
            pibrella.light.yellow.off()
        
        attemptingConnection = False
        

# Setup initial states
pibrella.light.green.off()
pibrella.light.yellow.off()
pibrella.light.red.on()

wiimote = None
attemptingConnection = False
pibrella.button.changed(handleConnectBtnPress)

button_delay = 0.2

while True:
    if (wiimote != None):
        buttons = wiimote.state['buttons']

        # If Plus and Minus buttons pressed
        # together then rumble and disconnect Wiimote.
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):              
            pibrella.light.green.off()
            pibrella.light.red.on()
            wiimote.rumble = 1
            time.sleep(1)
            wiimote.rumble = 0            
            wiimote.close()
            wiimote = None            

        # Turn left - (engage right motor only)
        if (buttons & cwiid.BTN_LEFT):
            pibrella.output.e.on()
            time.sleep(button_delay)
            pibrella.output.e.off()                     

        # Turn right - (engage left motor only)            
        if(buttons & cwiid.BTN_RIGHT):            
            pibrella.output.f.on()
            time.sleep(button_delay)
            pibrella.output.f.off()          

        # Go forward - (engage both motors)            
        if (buttons & cwiid.BTN_UP):            
            pibrella.output.e.on()
            pibrella.output.f.on()        
            time.sleep(button_delay)
            pibrella.output.e.off()
            pibrella.output.f.off()          
    else:    
        time.sleep(0.1)
