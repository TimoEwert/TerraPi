#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import lcd
import os, sys
from time import sleep
import time
import RPi.GPIO as GPIO
import board 
from adafruit_bme280 import basic as adafruit_bme280

deviceID = ['/sys/bus/w1/devices/28-0000073be7d4/w1_slave']
devicePurpose = ['Temp_ds18b20:']

i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
red=12
GPIO.setup(red,GPIO.OUT)
my_pwm=GPIO.PWM(red,100)
my_pwm.start(0)

#################################################################################################
##### FUNCTIONS #################################################################################
#################################################################################################
def setup():
  lcd.initialize()

def loop():
  for index in range(len(deviceID)):
  
    
    DS18B20 = getTemp(deviceID[index])
    tempDS18B20=DS18B20
    HumidityBME280="%0.0f" % bme280.relative_humidity
    fanstatus=luefter(HumidityBME280)
    TempBMe280="%0.0f" % bme280.temperature
    
    lcd.printString("W\xE1rme Spot: " + tempDS18B20 + chr(223) + "C", lcd.LINE_1)
    ldc.printString("Fanstatus: " + fanstatus,lcd.LINE_2)
    lcd.printString("Temperatur: " + TempBMe280 + chr(223) + "C", lcd.LINE_3)
    lcd.printString("Luftfeuchtigkeit:" + HumidityBME280 + "%", lcd.LINE_4)
    
    sleep(1)

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
        sntemp= False
    
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
