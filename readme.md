# Terrarium Control

## Features
This short script reads temperatures and humidity in a terrarium, sets a fan to certain speeds based on the temperature and shows the values ​​on an LCD display.
At the moment 10 rainy seasons can be set in the configuration.
then, after each rain, ventilation is carried out for period x in order to dry the windows. There is also a telegram notification for the steps
- Mainlight on / off
- Heat Spot on / off
- Rain on / off
- Ventilation after rain on / off

## Used Hardware
- [Raspberry Pi 3B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)
- [IRF520 MOSFET MODULE](https://www.amazon.de/gp/product/B01F3I9QDU)
- [DS18B20 temperature sensor](https://www.amazon.de/gp/product/B07GZWMCBM)
- [20x4 I2C LCD Display](https://www.amazon.de/gp/product/B0859YY2NZ)
- [Bequiet Pc fan](https://www.amazon.de/gp/product/B00IOIJ4AC)
- [Adafruit BME280](https://www.reichelt.de/de/de/entwicklerboards-temperatur-feuchtigkeits-und-drucksensor--debo-sens-thd-p235476.html)
- [Shelly 1 WiFi Switch](https://www.amazon.de/Shelly-Schalter-Wireless-Hausautomation-Anwendung/dp/B07G33LNDY/)

## Installation

### Install python3 and necessary python3 modules:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
sudo pip3 install adafruit-circuitpython-bme280 
```

### Clone this repository
`git clone git@github.com:TimoEwert/TerraPi.git`

### Go into the newly created TerraPi folder 
copy/rename the `.env-samplefile` to `.env` and edit the values to your needs


## Run the script
`python3 terrapi.py`

