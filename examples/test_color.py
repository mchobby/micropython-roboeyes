# RoboEyes for MicroPython - Basic test example
# This example shows how to use change the default colors to create a negative display
#
# Hardware:
#    You'll need a breadboard, a Raspberry-Pi Pico, a FrameBuffer
#    based diplsay (like I2C SSD1306 oled and some jumper wires.
#
# See MicroPython implementation at 
#    https://github.com/mchobby/micropython-roboeyes
#
# Ported from Arduino https://github.com/FluxGarage/RoboEyes
#   Arduino example Published in September 2024 by Dennis Hoelscher, FluxGarage
#   www.youtube.com/@FluxGarage
#   www.fluxgarage.com
#

from machine import I2C, Pin
from roboeyes import *
import ssd1306
import time

# Raspberry-Pi Pico - I2C(1)
i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )

# Adafruit 938 : Monochrome 1.3" 128x64 OLED graphic display - SSD1306
# SSD1306_I2C is a descendant of FrameBuf 
lcd = ssd1306.SSD1306_I2C( 128, 64, i2c, addr=0x3d )

# RoboEyes callback event
def robo_show( roboeyes ):
	global lcd
	lcd.show()

# Plug RoboEyes on any FrameBuffer descendant
#   Set foregroung color to BLACK
#   Set background color to WHITE
# This example use 1 bit color but for color can be defined with (r,g,b) or 16bit integer for color displays
robo = RoboEyes( lcd, 128, 64, frame_rate=100, on_show = robo_show, fgcolor=0, bgcolor=1 )

# Define some automated eyes behaviour
robo.set_auto_blinker( ON, 3, 2) # Start auto blinker animation cycle -> bool active, int interval, int variation -> turn on/off, set interval between each blink in full seconds, set range for random interval variation in full seconds
robo.set_idle_mode( ON, 2, 2) # Start idle animation cycle (eyes looking in random directions) -> turn on/off, set interval between each eye repositioning in full seconds, set range for random time interval variation in full seconds

while True:
	# update eyes drawings
	robo.update()  

	# Dont' use sleep() or sleep_ms() here in order to ensure fluid eyes animations.
 	# Check the AnimationSequences example for common practices.
