#!/bin/sh
# Install the files on a pico
if [ -z "$1" ]
  then
    echo "/dev/ttyACMx parameter missing!"
		exit 0
fi

mpremote connect $1 fs mkdir lib

echo "Installing common libraries"
# Getting micropython-lib/micropython/drivers/display/ssd1306/ssd1306.py
wget https://raw.githubusercontent.com/micropython/micropython-lib/refs/heads/master/micropython/drivers/display/ssd1306/ssd1306.py -O lib/ssd1306.py
mpremote connect $1 fs cp lib/ssd1306.py :lib/
mpremote connect $1 mip install github:mchobby/esp8266-upy/FBGFX
mpremote connect $1 mip install github:mchobby/micropython-roboeyes


echo "Installing RoboEyes  lib on Pico @ $1"
#mpremote connect $1 fs cp lib/*.py :lib/
#mpremote connect $1 fs cp lib/sim76xx/*.py :lib/sim76xx/

#echo "Copying main.py file"
#mpremote connect $1 fs cp main.py :main.py

echo " "
echo "Done!"
