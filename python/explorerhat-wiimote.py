#
# explorerhat-wiimote.py
#
# Use a Wiimote to control LEDs and motors via an ExplorerHAT for Raspberry Pi
# 
# In this example, the right side motor is connected to motor 1 and the left to motor 2
# Currently the script allows explicit connection and disconnection of the Wiimote, but unexpected
# disconnection might leave things in a strange state.

import cwiid
import explorerhat
import time

# Define speeds for ExplorerHAT - when mounted on the STS-PI, 100 is actually backwards, with -100 forwards
forwards = -100
backwards = 100
stopped = 0

# This method is called when the button 1 on the ExplorerHAT is pressed
def handleConnectBtnPress(channel, event):    
    global attemptingConnection
    global wiimote
    
    # Only attempt to connect if we aren't already connected, and not trying to connect
    if (wiimote == None and attemptingConnection == False):
    
        attemptingConnection = True
        explorerhat.light.green.off()
        explorerhat.light.red.off()
        explorerhat.light.yellow.pulse(0, 0, 1, 1)
        try:
            wiimote=cwiid.Wiimote()
            wiimote.rpt_mode = cwiid.RPT_BTN            
            explorerhat.light.green.on()
            explorerhat.light.yellow.off()
            wiimote.led = 1
        except RuntimeError:
            explorerhat.light.red.on()
            explorerhat.light.yellow.off()
        
        attemptingConnection = False
        

# Setup initial states
explorerhat.light.green.off()
explorerhat.light.yellow.off()
explorerhat.light.red.on()

wiimote = None
attemptingConnection = False
explorerhat.touch.one.pressed(handleConnectBtnPress)

button_delay = 0.2

while True:
    if (wiimote != None):
        buttons = wiimote.state['buttons']

        # If Plus and Minus buttons pressed
        # together then rumble and disconnect Wiimote.
        if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):              
            explorerhat.light.green.off()
            explorerhat.light.red.on()
            wiimote.rumble = 1
            time.sleep(1)
            wiimote.rumble = 0            
            wiimote.close()
            wiimote = None            

        # Turn left - (engage right motor only)
        if (buttons & cwiid.BTN_LEFT):
            explorerhat.motor.one.speed(forwards)
            time.sleep(button_delay)
            explorerhat.motor.one.speed(stopped)

        # Turn right - (engage left motor only)            
        if(buttons & cwiid.BTN_RIGHT):            
            explorerhat.motor.two.speed(forwards)
            time.sleep(button_delay)
            explorerhat.motor.two.speed(stopped)

        # Go forward - (engage both motors)            
        if (buttons & cwiid.BTN_UP):            
            explorerhat.motor.one.speed(forwards)
            explorerhat.motor.two.speed(forwards)
            time.sleep(button_delay)
            explorerhat.motor.one.speed(stopped)
            explorerhat.motor.two.speed(stopped)
            
        # Go backwards - (engage both motors in reverse)            
        if (buttons & cwiid.BTN_DOWN):            
            explorerhat.motor.one.speed(backwards)
            explorerhat.motor.two.speed(backwards)
            time.sleep(button_delay)
            explorerhat.motor.one.speed(stopped)
            explorerhat.motor.two.speed(stopped)
        
    else:    
        time.sleep(0.1)
