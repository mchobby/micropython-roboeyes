# RoboEyes library for MicroPython

Once upon a time, I browsed the internet and discovered the [RoboEyes video from FluxGarage](https://www.youtube.com/playlist?list=PLD2oXF44y-hLKjw_es2Vw1ycwBRNZ6ceE) on YouTube.

![Credit: RoboEyes for Arduino by [FluxGarage.com](https://www.fluxgarage.com/index.php)](docs/_static/roboeyes-01.jpg)


RoboEyes is open source library draws smoothly animated robot eyes on OLED displays (using the GFX library). It offers configurable eye shapes, several mood types and animations to add that certain kind of personality to your robot.

![Credit: RoboEyes moods by [FluxGarage.com](https://www.fluxgarage.com/index.php)](docs/_static/roboeyes-00.jpg)


The eyes was so lovely but unfortunately, the [library was written for Arduino Uno](https://github.com/FluxGarage/RoboEyes) by [FluxGarage](https://www.fluxgarage.com/index.php) and I'm a MicroPython addict.

__This library is a MicroPython portage of RoboEyes for Arduino__. 

Some enhancement was added into the library like:

* Based on MicroPython's FrameBuffer (so __works with 99% of displays__)
* Monochrome and color displays! 1 bit color by default (for OLED).
* Adding FROZEN, SCARY, CURIOUS moods to the exising DEFAULT, TIRED, ANGRY, HAPPY.
* Adding the wink() animation.
* Managing animation sequence (see [test_anim_sequence.py](examples/test_anim_sequence.py) ).

# Library 

The RoboEyes library and its dependencies must be copied to the MicroPython board before using the examples.

Dependencies are:

* GFX library for MicroPython
* Display driver (SSD1306 for most of OLED screen)

On a WiFi based plateform:
```
>>> import mip
>>> mip.install("github:mchobby/micropython-roboeyes")
>>> mip.install("github:mchobby/esp8266-upy/FBGFX")
```

Or via the `mpremote` utility:
```
mpremote mip install github:mchobby/micropython-roboeyes
mpremote mip install github:mchobby/esp8266-upy/FBGFX
```

The SSD1306 library is available in the official MicroPython repository. You can download it into and transfert it to your MicroPython board. 

Here the instruction used in [install.sh](install.sh) bash script.

```
$ wget https://raw.githubusercontent.com/micropython/micropython-lib/refs/heads/master/micropython/drivers/display/ssd1306/ssd1306.py -O lib/ssd1306.py
$ mpremote connect $1 fs cp lib/ssd1306.py :lib/
```


# Wiring 
As said, this FrameBuffer implementation of RoboEyes should work with any display (OLED, RGB, etc).

## Wiring to I2C OLED
Qwiic (SparFun) or StemmaQt (Adafruit Industries) is a standardized 4 pins connector shipping I2C bus (sda, scl) as well as power and ground.

Here a wiring via a [Qwiic-to-wire cable](https://shop.mchobby.be/fr/jst-sh/2429-cable-jst-sh-4-poles-vers-broches-males-150mm-stemma-qt-qwiic-3232100024298-adafruit.html) used for prototyping. The OLED screen used is the [Adafruit 128x64 OLED display - 1.3" Monochrome - I2C - StemmaQT / Qwiic](https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/307-afficheur-oled-128x64-13-monochrome-i2c-stemmaqt-qwiic-3232100003071-adafruit.html)

![oled to Raspberry-Pi Pico Wiring](docs/_static/qwiic-oled-to-pico-rp2040.jpg)

The OLED can be directly plugged with [qwiic wire](https://shop.mchobby.be/fr/jst-sh/2112-cable-jst-sh-4-poles-100mm-stemma-qt-qwiic-3232100021129-adafruit.html) on a microcontroler/board exposing a Qwiic connector.

![oled to Raspberry-Pi Pico Wiring](docs/_static/qwiic-stemmaQt.jpg)

# API

The RoboEyes API is described in the [MicroPython-RoboEyes-API.md](MicroPython-RoboEyes-API.md) document

# Examples

The repository comes with examples ported from Flux garage. Examples are mainly tested on 128x64 I2C capable OLED.

* [test_basic.py](examples/test_basic.py) : Simple script that can be used to test each features, one at the time.
* [test_color.py](examples/test_color.py) : show how to define colors when creating RoboEyes object.
* [test_anim_sequence.py](examples/test_anim_sequence.py) : create animation sequence without using delay.

Other examples:
* [test_round.py](examples/test_round.py) : create round eyes with negative spacing.
* [test_cyclops.py](examples/test_cyclops.py) : create a square cyclops eye.