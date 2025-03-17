# RoboEyes for MicroPython - Interactive Configuration example
#
# Allows to cycle accross the various properties/behaviours 
# of roboEyes and to interactively update their values 
#
# Hardware:
#    You'll need a breadboard, a Raspberry-Pi Pico, a FrameBuffer
#    based diplsay (like I2C SSD1306 oled, 3 PUSH_BUTTONS and 
#    some jumper wires.
#
#    Push-Buttons are use to place the GP19 (-), GP20 (enter/exit), GP21 (+)
#    inputs to the Ground.
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
from time import ticks_ms, ticks_diff

# -----------------------------------------------------------------
#   Manage the Buttons
#------------------------------------------------------------------
DEBOUNCE_MS = 300

plus_count = 0 # increment with IRQ raised on the input (-) button
ok_count = 0
minus_count = 0 
last_click = ticks_ms()
def btn_plus_cb( btn ):
	global plus_count,last_click
	if ticks_diff( ticks_ms(), last_click )<DEBOUNCE_MS:
		return
	plus_count += 1
	last_click = ticks_ms()
def btn_ok_cb( btn ):
	global ok_count,last_click
	if ticks_diff( ticks_ms(), last_click )<DEBOUNCE_MS:
		return
	ok_count += 1
	last_click = ticks_ms()
def btn_minus_cb( btn ):
	global minus_count,last_click
	if ticks_diff( ticks_ms(), last_click )<DEBOUNCE_MS:
		return		
	minus_count += 1
	last_click = ticks_ms()
btn_plus = Pin( Pin.board.GP21, Pin.IN, Pin.PULL_UP )
btn_ok   = Pin( Pin.board.GP20, Pin.IN, Pin.PULL_UP )
btn_minus= Pin( Pin.board.GP19, Pin.IN, Pin.PULL_UP )
btn_plus.irq( btn_plus_cb, Pin.IRQ_FALLING )
btn_ok.irq( btn_ok_cb, Pin.IRQ_FALLING )
btn_minus.irq( btn_minus_cb, Pin.IRQ_FALLING )

def plus_pressed():
	global plus_count
	_r = plus_count > 0
	plus_count = 0
	return _r

def ok_pressed():
	global ok_count
	_r = ok_count > 0
	ok_count = 0
	return _r

def minus_pressed():
	global minus_count
	_r = minus_count > 0
	minus_count = 0
	return _r

# -----------------------------------------------------------------
#   Current Option and value
#------------------------------------------------------------------

MOOD_LABEL = ["DEFAULT", "TIRED", "ANGRY", "HAPPY", "FROZEN", "SCARY", "CURIOUS"]
POSITION_LABEL = ["DEFAULT", "N", "NE", "E", "SE", "S", "SW", "W", "NW"]


# The tuple is ( option_label, option_short_label, get_curr_value(), set_increased_value() (+), set_decreased_value() (-)  ) 
OPTIONS = [ ("Auto Blinker", "A.Blinker", lambda robo: True if robo.autoblinker else False, lambda robo: robo.set_auto_blinker(ON,3,2), lambda robo: robo.set_auto_blinker(OFF) ),
			("Auto Idle",    "A.Idle"   , lambda robo: True if robo.idle else False,        lambda robo: robo.set_idle_mode(ON,2,2),    lambda robo: robo.set_idle_mode(OFF)    ),
			("Eyes Width",   "Eyes.W"   , lambda robo: str(robo.eyeLwidthDefault),          lambda robo: robo.eyes_width(robo.eyeLwidthDefault+1,robo.eyeLwidthDefault+1),  lambda robo: robo.eyes_width(robo.eyeLwidthDefault-1,robo.eyeLwidthDefault-1)  ),
			("Eyes Height",  "Eyes.H"   , lambda robo: str(robo.eyeLheightDefault),         lambda robo: robo.eyes_height(robo.eyeLheightDefault+1,robo.eyeLheightDefault+1),  lambda robo: robo.eyes_width(robo.eyeLheightDefault-1,robo.eyeLheightDefault-1)  ),
			("Eyes Radius",  "Eyes.r"   , lambda robo: str(robo.eyeLborderRadiusDefault),   lambda robo: robo.eyes_radius(robo.eyeLborderRadiusDefault+1,robo.eyeLborderRadiusDefault+1),  lambda robo: robo.eyes_radius(robo.eyeLborderRadiusDefault-1,robo.eyeLborderRadiusDefault-1)  ),
			("Eyes Spacing", "Eyes.Sp"  , lambda robo: str(robo.spaceBetweenDefault),       lambda robo: robo.eyes_spacing(robo.spaceBetweenDefault+1), lambda robo: robo.eyes_spacing(robo.spaceBetweenDefault-1)  ),
			("Cyclops mode", "Cyclops"  , lambda robo: True if robo._cyclops else False,    lambda robo: robo.set_cyclops(True), lambda robo: robo.set_cyclops(False) ),
			("Select Mood" , "Mood"     , lambda robo: MOOD_LABEL[robo._mood],              lambda robo: robo.set_mood( robo._mood+1 if robo._mood<6 else robo._mood ), lambda robo: robo.set_mood( robo._mood-1 if robo._mood>0 else robo._mood ) ),
			("Position"    , "Position" , lambda robo: POSITION_LABEL[robo._position],      lambda robo: robo.set_position( robo._position+1 if robo._position<8 else robo._position ), lambda robo: robo.set_position( robo._position-1 if robo._position>0 else robo._position ) ) ,
			("Confuse & Laugh" , "(-)Conf (+)Laugh"  , lambda robo: "",                     lambda robo: robo.laugh(),    lambda robo: robo.confuse() ),
			("Wink"            , "(-)Left (+)Right"  , lambda robo: "",                     lambda robo: robo.wink(right=True), lambda robo: robo.wink(left=True) ),
			("Close & Open"    , "(-)Close (+)Open"  , lambda robo: "",                     lambda robo: robo.open(), lambda robo: robo.close() ),
			("Horiz flicker"   , "H.flicker"         , lambda robo: "%s %s"%(robo.hFlickerAmplitude, "ON" if robo.hFlicker else "off"), lambda robo: robo.horiz_flicker( True, robo.hFlickerAmplitude+1 ), lambda robo: robo.horiz_flicker( True if robo.hFlickerAmplitude-1>0 else  False , robo.hFlickerAmplitude-1 if robo.hFlickerAmplitude-1>0 else 0 ) ) ,
			("Vert flicker"    , "V.flicker"         , lambda robo: "%s %s"%(robo.vFlickerAmplitude, "ON" if robo.vFlicker else "off"), lambda robo: robo.vert_flicker( True, robo.vFlickerAmplitude+1 ), lambda robo: robo.vert_flicker( True if robo.vFlickerAmplitude-1>0 else  False , robo.vFlickerAmplitude-1 if robo.vFlickerAmplitude-1>0 else 0 ) ) ,
			("Left Eye Width"  , "L.Eye.W"           , lambda robo: str(robo.eyeLwidthDefault),  lambda robo: robo.eyes_width(leftEye=robo.eyeLwidthDefault+1),  lambda robo: robo.eyes_width(leftEye=robo.eyeLwidthDefault-1)  ),
			("Left Eye Height" , "L.Eye.H"           , lambda robo: str(robo.eyeLheightDefault), lambda robo: robo.eyes_height(leftEye=robo.eyeLheightDefault+1),  lambda robo: robo.eyes_height(leftEye=robo.eyeLheightDefault-1)  ),
			("Left Eye Radius" , "L.Eye.r"           , lambda robo: str(robo.eyeLborderRadiusDefault), lambda robo: robo.eyes_radius(leftEye=robo.eyeLborderRadiusDefault+1),  lambda robo: robo.eyes_radius(leftEye=robo.eyeLborderRadiusDefault-1)  ),
			("Right Eye Width" , "R.Eye.W"           , lambda robo: str(robo.eyeRwidthDefault),  lambda robo: robo.eyes_width(rightEye=robo.eyeRwidthDefault+1),  lambda robo: robo.eyes_width(rightEye=robo.eyeRwidthDefault-1)  ),
			("Right Eye Heigh" , "R.Eye.H"           , lambda robo: str(robo.eyeRheightDefault), lambda robo: robo.eyes_height(rightEye=robo.eyeRheightDefault+1),  lambda robo: robo.eyes_height(rightEye=robo.eyeRheightDefault-1)  ),
			("Right Eye Radiu" , "R.Eye.r"           , lambda robo: str(robo.eyeRborderRadiusDefault), lambda robo: robo.eyes_radius(rightEye=robo.eyeRborderRadiusDefault+1),  lambda robo: robo.eyes_radius(rightEye=robo.eyeRborderRadiusDefault-1)  )
	]

option_index = 0
option_selected = False

# -----------------------------------------------------------------
#   RoboEyes
#------------------------------------------------------------------

i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )
lcd = ssd1306.SSD1306_I2C( 128, 64, i2c, addr=0x3d )

# RoboEyes callback event
def robo_show( roboeyes ):
	global lcd, option_index, option_selected

	# Text display on the display
	if not( option_selected ):
		text = '%s?' % OPTIONS[option_index][0]
	else:
		text = '%s=%s' % (OPTIONS[option_index][1], OPTIONS[option_index][2](roboeyes) )

	lcd.text(text, 0,56, roboeyes.fgcolor )
	lcd.show()

robo = RoboEyes( lcd, 128, 64, frame_rate=100, on_show = robo_show )


while True:
	if ok_pressed():
		# Enter/Exit
		option_selected = not( option_selected )

	if plus_pressed():
		if option_selected:
			# Make (+) call on the value of current option 
			OPTIONS[option_index][3]( robo )
		else:
			# select next option
			option_index += 1
			if option_index >= len(OPTIONS):
				option_index = 0

	if minus_pressed():
		if option_selected:
			# Make (-) call on the value of current option 
			OPTIONS[option_index][4]( robo ) 
		else:
			# select previous option
			option_index -= 1
			if option_index < 0:
				option_index = len(OPTIONS)-1

	# update eyes drawings
	robo.update()  

