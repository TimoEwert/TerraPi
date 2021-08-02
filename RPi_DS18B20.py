#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import lcd
import os, sys
from time import sleep
import time
import RPi.GPIO as GPIO

deviceID = ['/sys/bus/w1/devices/28-0000073be7d4/w1_slave']
devicePurpose = ['Temp_ds18b20:']

#################################################################################################
##### FUNCTIONS #################################################################################
#################################################################################################
def setup():
  lcd.initialize()

def loop():
  for index in range(len(deviceID)):
    fan = open("/home/pi/terrapi/fanstatus.txt","r")
    fanstatus = fan.read()
    humibme280data = open("/home/pi/terrapi/BME280_humidity_data.txt","r")
    humidity = humibme280data.read()
    tempbme280data = open("/home/pi/terrapi/BME280_temperature_data.txt","r")
    tempbme280 = tempbme280data.read()
    lcd.printString("W\xE1rme Spot: " + str(getTemp(deviceID[index])+chr(223)+"C"), lcd.LINE_1)
    lcd.printString("Fanstatus:   " + fanstatus, lcd.LINE_2)
    lcd.printString("Temperatur:     " + tempbme280+chr(223)+"C", lcd.LINE_3)
    lcd.printString("Luftfeuchtigkeit:" + humidity + "%", lcd.LINE_4)
    sleep(2)
#    lcd.clear()


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
