#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import lcd
import os, sys
from time import sleep
import time
import RPi.GPIO as GPIO

deviceID = ['/sys/bus/w1/devices/28-0000073be7d4/w1_slave']
devicePurpose = ['Temp_ds18b20:']

def loop():
    for index in range(len(deviceID)):
        tempprint = getTemp(deviceID[index])
        sleep(5)
        file = open("/home/pi/terrapi/DS18B20_data.txt","w")
        file.write(tempprint)
        file.close()
        print(tempprint)

def getTemp(ID):
    file = open(ID)
    rawData = file.read()
    file.close()

    rawValue = rawData.split("\n")[1].split(" ")[9]
    temperature = int(float(rawValue[2:]) / 1000)

    return '%i' % temperature

if __name__ == "__main__":
  while True:
    loop()

