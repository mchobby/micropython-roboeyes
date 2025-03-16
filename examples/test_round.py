# RoboEyes for MicroPython - create round eyes
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

robo = RoboEyes( lcd, 128, 64, frame_rate=100, on_show = robo_show )
# Define some automated eyes behaviour
robo.set_auto_blinker( ON, 3, 2) 
robo.set_idle_mode( ON, 2, 2) 
# Round Eye definition
robo.eyes_width(45, 45) 
robo.eyes_height(45, 45)
robo.eyes_radius(22, 22)
robo.eyes_spacing(-7)

while True:
	robo.update()  