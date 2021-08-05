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
ip_shelly=config["Configuration"]["ip_shelly1"]
rainduration=config["Configuration"]["rainduration"]
device=config["Configuration"]["device"]
sea_level_pressure=config["Configuration"]["sea_level_pressure"]
gpio_for_IRF520=config["Configuration"]["gpio_for_IRF520"]


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
def setup():
  lcd.initialize()

def loop():
    DS18B20 = getTemp(device)
    tempDS18B20=DS18B20
    rain()
    print(sea_level_pressure)
    HumidityBME280="%0.0f" % bme280.relative_humidity    
    fanstatus=luefter(HumidityBME280)
    TempBMe280="%0.0f" % bme280.temperature
    lcd.printString("W\xE1rme Spot: " + tempDS18B20 + chr(223) + "C", lcd.LINE_1)
    lcd.printString("Fanstatus: " + fanstatus,lcd.LINE_2)
    lcd.printString("Temperatur: " + TempBMe280 + chr(223) + "C", lcd.LINE_3)
    lcd.printString("Luftfeuchtigkeit:" + HumidityBME280 + "%", lcd.LINE_4)
    sleep(1)



def rain():    
    actualtime = datetime.datetime.now()
    actualtime = int(actualtime.strftime('%H%M'))
    if (actualtime == raintime):
        lcd.printString("Bew\xE1sserungsvorgang", lcd.LINE_2)
        my_pwm.ChangeDutyCycle(0)
        print("Bewässungsvorgang")
        requests.get("http://" + ip_shelly1 + "/relay/0?turn=on")
        sleep(rainduration)
        requests.get("http://" + ip_shelly1 + "/relay/0?turn=off")
        sleep(60)



def luefter(humidity):
    humidity=int(humidity)
    if(humidity >= 90):
        my_pwm.ChangeDutyCycle(100)
        fanstatus = ("ON 100%")
    elif(humidity >= 80):
        my_pwm.ChangeDutyCycle(75)
        fanstatus = ("ON 75%")
    elif(humidity >= 75):
        my_pwm.ChangeDutyCycle(50)
        fanstatus = ("ON 50%")
    elif(humidity >= 70):
        my_pwm.ChangeDutyCycle(30)
        fanstatus = ("ON 30%")
    elif(humidity < 70):
        my_pwm.ChangeDutyCycle(0)
        fanstatus = ("Off 0%")
    else:
        fanstatus = ("Off 0%")
        my_pwm.stop()
        GPIO.cleanup()

    return fanstatus


def getTemp(ID):
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
