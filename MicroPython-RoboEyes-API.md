# Introduction

This document describe the __RoboEyes__ and __Sequences__ classes.

# RoboEyes class

The RoboEyes is the main class used to control the properties and animation of the Eyes.

Note that `self`  is part of the Python class definition.

## \_\_init\_\_() method

Class constructor.


```
def __init__(self, fb, width, height, frame_rate=20, on_show=None, bgcolor=BGCOLOR, fgcolor=FGCOLOR ):
```

* __fb__ : FrameBuffer into which the RoboEyes will be drawed the Eyes.
* __width__ : Width of the FrameBuffer in Pixels
* __height__ : Height of the FrameBuffer in Pixels
* __frame_rate__ : Max frame rate to refresh the screen. Higher is the autorized rate, and smoother the animation will be.
* __on_show__ : callback event executed by RoboEyes when framebuffer data should be sent to the display.
* __bgcolor__ : color used for the background. This value is sent immediately to the FrameBuffer drawing routines.
* __fgcolor__ : color used for the foreground drawing.

Minimal setup example:

``` python 
from machine import I2C, Pin
from roboeyes import *
import ssd1306
import time

i2c = I2C( 1, sda=Pin.board.GP6, scl=Pin.board.GP7 )
lcd = ssd1306.SSD1306_I2C( 128, 64, i2c, addr=0x3d )

# RoboEyes callback event
def robo_show( roboeyes ):
	global lcd
	lcd.show()

robo = RoboEyes( lcd, 128, 64, frame_rate=100, on_show = robo_show )

while True:
	robo.update() 
```

## update() method

The `update` method is responsible for drawing each iteration of RoboEyes animation. The call to `update` only perform drawing at the proper timing to respect the desired frame_rate. The `update` method is also responsible to trigger the `on_show` event.

When called to early the method will simply return execution to the callee. 

The `update` method is also responsible to schedule the steps of a started sequence (see later in this document)

Do not hesitate to call `update` as often as possible. 

## set_auto_blinker() method

Set automated eye blinking with minimal blink interval and blink interval variation range.

Note that set_auto_blinker() must be disabled when using the `close()` and `open()` methods.

``` python
def set_auto_blinker( self, active, interval=None, variation=None):
```

* __active__ : use the constant ON and OFF. When activating, the `interval` (default 1) and `variation` (default 4) should ne set.
* __interval__ : minimum interval between 2 consecutive blink (in seconds).
* __variation__ : maximum random time to add to `interval` for the next blink (in seconds).

Example: 

``` python 
robo.set_auto_blinker( ON, 3, 2)
```

## set_idle_mode() method

Set automated eye repositioning with minimal time interval and time interval variation range.

``` python
def set_idle_mode( self, active, interval=None, variation=None)
```

* __active__ : use the constant ON and OFF. When activating, the `interval` (default 1) and `variation` (default 4) should ne set.
* __interval__ : minimum interval between 2 consecutive repositionning (in seconds).
* __variation__ : maximum random time to add to `interval` for the next repositionning (in seconds).

Example: 

``` python 
robo.set_idle_mode( ON, 2, 2)
```
## EYE GEOMETRY

### eyes_width() method

Set the width of each eyes.  Default value is 45 pixels.

```
def eyes_width( self, leftEye, rightEye)
```

Here an example of distinct eye width and eye height.

![Distinct height & width for each eye](docs/_static/interactive-value-01.jpg)

### eyes_height() method

Set the height of each eye. The default value is 45 pixels.

```
def eyes_height( self, leftEye, rightEye )
```


### eyes_radius() method

Define the radius to apply on corners of each eye. The default value is 8 pixels.

Using a 0 pixel radius will show __SQUARE eye__. Having `Height = Width` and `radius = Height / 2` will show a __ROUND eye__.


```
def eyes_radius( self, leftEye, rightEye)
```

Here an example of disctinct radius value.

![Distinct radius for each eye](docs/_static/radius-eyes.jpg)

### eyes_spacing() method

Set the space between the both eyes. The default value is 10 pixels.

Space can be lower and negative, giving a very special look to your eyes.

```
def eyes_spacing( self, space )
```

Example:

``` Python
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
robo.eyes_radius(8, 8)
robo.eyes_radius(22, 22)
robo.eyes_spacing(-7)

while True:
	robo.update()  
```

Which produce the following eyes.

![Round Eyes with negative spacing](docs/_static/round-eyes.jpg)

### Sequences property

Give access to various sequence. See the definition of the `Sequences` class.

### cyclops property

Setting the `cyclops` boolean property will activate the Cyclop mode (show only one eyes).

```
@cyclops.setter
def cyclops( self, enabled ):
```

Notice: the `def set_cyclops( self, value )` can be used for creating lambda expression.

``` python
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
# Cyclop Eye definition
robo.eyes_width(20, 20) 
robo.eyes_height(45, 45)
robo.eyes_radius(0, 0)
robo.cyclops = True

while True:
	robo.update()  
```

Which produce the following eye.

![Cyclops Eye](docs/_static/cyclops-eye.jpg)


## mood property

Setting the `mood` property will update the dynamic eyes behaviour.

The possible values are the following constants: __DEFAULT, TIRED, ANGRY, HAPPY, FROZEN, SCARY, CURIOUS__.

```
@mood.setter
def mood( self, mood )
```

Notice: the `def set_mood( self, mood )` can be used for creating lambda expression.


The __DEFAULT__ value is the default mode where eyes a usually open.

The __TIRED__ will partially close the eyelid on the eyes.

The __ANGRY__ will make the eyebrows pointing back between the eyes.

The __HAPPY__ will curves/bump up the eyes.

The __FROZEN__ will make eyes slightly shaking from left-to-right (like your head would do when you are frozen).

The __SCARY__ will partially close the eyes and made it slightly shaking from top-to-bottom (like your jaw would do if you are afraid).

The __CURIOUS__ will increase the size of the eye near of the left or right border (behind the scene, this activates the `curious` property).


Example:

``` python
robo.mood = HAPPY 
```


## position property

Move the eyes on a given border/corner of the screen accordingly to the value __N, NE, E, SE, S, SW, W, NW__. The value __DEFAULT__ can be used to horizontally and vertically centered the eye.

```
@position.setter
def position( self, direction )
```

Compatible with an active `set_idle_mode()`, eye will start moving again after the eyes had moved in the target position. 

Notice: the `def set_position( self, direction )` can be used for creating lambda expression.


Example:

``` python
robo.position = SW 
```


## curious property

Set curious mode as the `robo.mood=CURIOUS` would do with a True / False parameter.

The respectively outer eye gets larger when looking left or right.

``` python
curious.setter
def curious( self, enable )
```

Notice: the `def set_curious( self, enable )` can be used for creating lambda expression.


## confuse() method

Make the eyes flicker left-and-right in a rather large distance (20 pixels) like shaking the head. 

The animation duration is about 500 ms.

``` python
def confuse( self )
```


## laugh() method 

Make the eyes jumping up and down (like laughing out loud) for 500 ms. This short animation is played once.

Notice that setting the `mood` to __HAPPY__ would gives a great result.

``` python
def laugh( self )
```


## blink() method

Activate eye blink sequence. This call make sense only when autoblinker is disable.

``` python
def blink( self, left=None, right=None )
```


## wink() method
Make either a left, either a right eye wink.

This call __disable the autoblinker and idle mode__.

``` python
def wink( self, left=None, right=None )
```

Example:

``` python
robo.wink( right=True )
```


## open() & close() method

Open or close the eyes. When closed, the eyes are reduced to a single line.

__Idle mode must be disabled__ when using thoses methods. See the [test_anim_sequence.py](examples/test_anim_sequence.py) .


## horiz_flicker() method

horizontal Eyes shaking/flickering. This basic method is used for several effect (eg: FROZEN mood).

``` python
def horiz_flicker( self, enable, amplitude=None )
```
* __enable__ : True/False to activate/deactivate horizontal Eyes flickering.
* __amplitude__ : flickering amplitude in pixels.


## vert_flicker() method

Same as `horiz_flicker()` but for vertical movement.


# Sequences class

The Sequences class is a list containing `Sequence`. Each `Sequence` contains a list of __Step__ (formmally `StepData` class).

The `RoboEyes.sequences` is used to define several `Sequence` (a `Sequence` is like one animation). 

Each `Sequence` can be started at any time by calling its `start()` method. When started, the `sequence` executes its various steps it contains, execution made at the right timing. 

Example:

The following code defines the `Sequence` named "demo" and the various steps it contains.

``` python
robo = RoboEyes( lcd, 128, 64, frame_rate=100, on_show = robo_show )

# RoboEyes can store several animation sequences 
#   Lets create the sequence ZERO
seq = robo.sequences.add( "demo" )
seq.step( 2000, lambda robo : robo.open() ) # at 2000 ms from start --> open eyes.
seq.step( 4000, lambda robo : robo.set_mood(HAPPY) ) # Lamba must call function! Cannot assign property! 
seq.step( 4010, lambda robo : robo.laugh() )
seq.step( 6000, lambda robo : robo.set_mood(TIRED) )
seq.step( 8000, lambda robo : robo.set_mood(DEFAULT) )
seq.step( 9000, lambda robo : robo.close() )
seq.step( 10000, lambda robo : print(seq.name,"done !") )  # Also signal the end of sequence at 10 sec
```

## add() method 

This method is called prior to define a new sequence of step (say: to define a new "animation").

Create a `Sequence` object, give it a name and register it into the `Sequences` list. 

The method returns a reference to the created `Sequence` objet. 

``` python 
def add( self, name  )
```


## done property

Check if all defined `Sequence` are done. The property is True when all started `Sequence` are done! (Note: a not started `Sequence` is always done).

``` python
@property
def done( self )
```


## update() method

That method check if any started `Sequence` it contains have a pending __Step__ to execute. If such then the pending __Step__ are executed.

``` python
def update( self )
```

# Sequence class

The `Sequence` class is container of __Step__ s (`StepData`). Each __Step__ defines a task to perform at a given time (after Sequence is started).


## step() method 

This method is used to add the definition of new __Step__ into the sequence.

``` python
def step( self, ms_timing, _lambda )
```
	
* __ms_timing__ : time in milliseconds after the Sequence start. Time when the __Step__ must be executed.
* __\_lambda__ : the function to execute. Must be a function or lambda expression receiving a RoboEyes instance as parameter.

As the \_lambda receives the robo (RoboEyes instance), the step can run action (method call) to change the Eyes behavior, mood, animation, etc.

Due to the limitation of the MicroPython parser, the lambda expression cannot make property assignation. This is the raison why the RoboEyes properties hase their equivalent `set_xxx()` method.

In the following lines:

``` python
seq.step( 6000, lambda robo : robo.set_mood(TIRED) )
seq.step( 8000, lambda robo : robo.set_mood(DEFAULT) )
```

The mood of the RoboEyes will be set to TIRED 6 seconds after the start of the sequence. The mood will be changed again to DEFAULT 8 seconds after the sequence start.

The `Sequence` will be set to "done" immediately after execution of the last __Step__. 

IF the `Sequence` must last longer than last step execution THEN just add a final step with a `print()` statement. That will delay the end of sequence execution until the `print()` is executed.


## start() method

Start the execution of the `Sequence`... meaning the execution of the __Step__ contained into the `Sequence`.

This method also set the _start_ flag and keeps track of the starting time (required to executes the __Step__ at the right time).


## reset() method

Reset the _start_ flag of the sequence as well as the `done` flag of all the __Step__ .

``` python
def reset( self )
```

## done property

Return `True` when all the steps of a started sequence are executed (are `done`).

A not started `Sequence` is always `done`! So the property return False only when one or more steps to be executed.

``` python
@property
def done( self )
```

## Update() method

Check if one of the defined __Step__s have to be executed. If so, it does it by calling the step.update().
