#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import lcd
import os, sys
from time import sleep
import time
import RPi.GPIO as GPIO
import board 
from adafruit_bme280 import basic as adafruit_bme280
import requests
import configparser
import datetime

config = configparser.ConfigParser()
config.read(".env")

raintime=config["Configuration"]["raintime"]
ip_shelly1=config["Configuration"]["ip_shelly1"]
rainduration=config["Configuration"]["rainduration"]
device=config["Configuration"]["device"]
sea_level_pressure=config["Configuration"]["sea_level_pressure"]
gpio_for_IRF520=int(config["Configuration"]["gpio_for_IRF520"])


i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = sea_level_pressure

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(gpio_for_IRF520,GPIO.OUT)
my_pwm=GPIO.PWM(gpio_for_IRF520,100)
my_pwm.start(0)

#################################################################################################
##### FUNCTIONS #################################################################################
#################################################################################################

###LCD Display initialize
def setup():
  lcd.initialize()
  
###Mainloop
def loop():
    DS18B20 = getTemp_DS18B20(device)
    tempDS18B20=DS18B20
    rain()
    HumidityBME280="%0.0f" % bme280.relative_humidity
    TempBMe280="%0.0f" % bme280.temperature
    fanstatus=fan(TempBMe280)
    lcd.printString("W\xE1rme Spot: " + tempDS18B20 + chr(223) + "C", lcd.LINE_1)
    lcd.printString("Fanstatus: " + fanstatus,lcd.LINE_2)
    lcd.printString("Temperatur: " + TempBMe280 + chr(223) + "C", lcd.LINE_3)
    lcd.printString("Luftfeuchtigkeit:" + HumidityBME280 + "%", lcd.LINE_4)
    sleep(1)
    
###Rain function for Rain at specific times config "raintime" for times to rain
def rain():    
    actualtime = datetime.datetime.now()
    actualtime = int(actualtime.strftime('%H%M'))
    if (actualtime == raintime):
        lcd.printString("", lcd.LINE_1)
        lcd.printString(" Bew\xE1sserungsvorgang",lcd.LINE_2)
        lcd.printString("L\xF5fter l\xE1uft auf 100%", lcd.LINE_3)
        lcd.printString(actualtime, lcd.LINE_4)
        my_pwm.ChangeDutyCycle(0)
        requests.get("http://" + ip_shelly1 + "/relay/0?turn=on")
        sleep(rainduration)
        requests.get("http://" + ip_shelly1 + "/relay/0?turn=off")
        sleep(60)
        
###Fan temperature control with change dutycycle for specific temperatures
def fan(temp_bme280):
    temp_bme280=int(temp_bme280)
    if(temp_bme280 >= 30):
        my_pwm.ChangeDutyCycle(100)
        fanstatus = ("ON 100%")
    elif(temp_bme280 >= 29):
        my_pwm.ChangeDutyCycle(75)
        fanstatus = ("ON 75%")
    elif(temp_bme280 >= 28):
        my_pwm.ChangeDutyCycle(50)
        fanstatus = ("ON 50%")
    else:
        fanstatus = ("Off 0%")
        my_pwm.stop()
        GPIO.cleanup()
    return fanstatus

###DS18B20 getting Temperature function
def getTemp_DS18B20(ID):
  file = open(ID)
  rawData = file.read()
  file.close()
  rawValue = rawData.split("\n")[1].split(" ")[9]
  temperature = int(float(rawValue[2:]) / 1000)
  return '%6.2f' % temperature
#################################################################################################
##### MAIN ######################################################################################
#################################################################################################
if __name__ == "__main__":
  setup()
  while True:
    loop()
#################################################################################################
##### END OF CODE ###############################################################################
#################################################################################################
