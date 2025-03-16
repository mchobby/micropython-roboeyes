# RoboEyes for MicroPython - Basic test example
# This example shows how to use the basic methods of the Robo Eyes library
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

# Start the display
lcd.fill(1)
lcd.show() 
time.sleep_ms( 300 )


# RoboEyes callback event
def robo_show( roboeyes ):
	global lcd
	lcd.show()

# Plug RoboEyes on any FrameBuffer descendant
robo = RoboEyes( lcd, 128, 64, frame_rate=100, on_show = robo_show )

# Define some automated eyes behaviour
robo.set_auto_blinker( ON, 3, 2) # Start auto blinker animation cycle -> bool active, int interval, int variation -> turn on/off, set interval between each blink in full seconds, set range for random interval variation in full seconds
robo.set_idle_mode( ON, 2, 2) # Start idle animation cycle (eyes looking in random directions) -> turn on/off, set interval between each eye repositioning in full seconds, set range for random time interval variation in full seconds

# --[ Define eye shapes, all values in pixels ]--
#robo.eyes_width(28, 28) # byte leftEye, byte rightEye
#robo.eyes_height(45, 45) # byte leftEye, byte rightEye
#robo.eyes_radius(8, 8) # byte leftEye, byte rightEye
#robo.eyes_radius(18, 18) # byte leftEye, byte rightEye (looking round when height=width=36)
#robo.eyes_spacing(10) # int space between eyes-> can also be negative

# --[ Cyclops mode ]--
# robo.cyclops = True  #  if turned on, robot has only on eye

# --[ Initial setup animation ]-- 
# Give a second to the eyes to open in their default state
start = time.ticks_ms()
while time.ticks_diff( time.ticks_ms(), start ) < 1000 :
	robo.update()  

# --[ Open/Close Eyes ]-- 
# Auto blinker must be disable to properly run this
#robo.close() # Close Eyes
#robo.open() # Open Eyes

# --[ Define mood, curiosity and position ]--
#robo.mood = DEFAULT  # mood expressions, can be TIRED, ANGRY, HAPPY, FROZEN, AFRAID, CURIOUS, DEFAULT
#robo.position = DEFAULT # cardinal directions, can be N, NE, E, SE, S, SW, W, NW, DEFAULT (default = horizontally and vertically centered)

#robo.curious = True  # bool on/off -> when turned on, height of the outer eyes increases when moving to the very left or very right

# --[ Set horizontal or vertical flickering ]--
#robo.horiz_flicker(True, 2) # bool on/off, byte amplitude -> horizontal flicker: alternately displacing the eyes in the defined amplitude in pixels
#robo.vert_flicker(True, 2) # bool on/off, byte amplitude -> vertical flicker: alternately displacing the eyes in the defined amplitude in pixels

# --[ Play prebuilt oneshot animations ]--
#robo.confuse() # confused - eyes shaking left and right
#robo.laugh() # laughing - eyes shaking up and down
#robo.wink( right=True ) # make the right Eye Winking

while True:
	# update eyes drawings
	robo.update()  

	# Dont' use sleep() or sleep_ms() here in order to ensure fluid eyes animations.
 	# Check the AnimationSequences example for common practices.
