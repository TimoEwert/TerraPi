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
import json

###Edit config file (.env) to change parameters
config = configparser.ConfigParser()
config.read("/home/pi/TerraPi/.env")

raintime1=int(config["Configuration"]["raintime1"])
raintime2=int(config["Configuration"]["raintime2"])
raintime3=int(config["Configuration"]["raintime3"])
raintime4=int(config["Configuration"]["raintime4"])
raintime5=int(config["Configuration"]["raintime5"])
raintime6=int(config["Configuration"]["raintime6"])
raintime7=int(config["Configuration"]["raintime7"])
raintime8=int(config["Configuration"]["raintime8"])
raintime9=int(config["Configuration"]["raintime9"])
raintime10=int(config["Configuration"]["raintime10"])

bot_token=config["Configuration"]["bot_token"] ###token for Telegram Bot
bot_chatID=config["Configuration"]["bot_chatID"] ###ChatID for Telegram Bot
ip_shelly1=config["Configuration"]["ip_shelly1"] ###Shelly for rain
ip_shelly2=config["Configuration"]["ip_shelly2"] ###Shelly for main light
ip_shelly3=config["Configuration"]["ip_shelly3"] ###Shelly for heating Spot
rainduration=int(config["Configuration"]["rainduration"])
device=config["Configuration"]["device"]
sea_level_pressure=config["Configuration"]["sea_level_pressure"]
gpio_for_IRF520=int(config["Configuration"]["gpio_for_IRF520"])
mainlight_on=int(config["Configuration"]["mainlight_on"])
mainlight_off=int(config["Configuration"]["mainlight_off"])
heatlight_on=int(config["Configuration"]["heatlight_on"])
heatlight_off=int(config["Configuration"]["heatlight_off"])
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
  rain()
  mainlight_timer()
  heating_spot_timer()
  tempDS18B20=getTemp_DS18B20(device)
  HumidityBME280="%0.0f" % bme280.relative_humidity
  TempBME280="%0.0f" % bme280.temperature
  fanstatus=fan(TempBME280)
  lcd.printString("W\xE1rme Spot: " + tempDS18B20 + chr(223) + "C", lcd.LINE_1)
  lcd.printString("L\xF5fter: " + fanstatus,lcd.LINE_2)
  lcd.printString("Temperatur: " + TempBME280 + chr(223) + "C", lcd.LINE_3)
  lcd.printString("Luftfeucht.:" + HumidityBME280 + "%", lcd.LINE_4)
  sleep(1)

###Lightning timer for shelly2 Main Light
def mainlight_timer():
  actualtime = datetime.datetime.now()
  actualtime = int(actualtime.strftime('%H%M'))
  if(actualtime == mainlight_on):
    requests.get("http://" + ip_shelly2 + "/relay/0?turn=on")
    telegram("Arcardia LED an")
    sleep(60)
  elif(actualtime == mainlight_off):
    requests.get("http://" + ip_shelly2 + "/relay/0?turn=off")
    telegram("Arcardia LED aus")
    sleep(60)
###Lightning timer for shelly3 Heating Spot
def heating_spot_timer():
  actualtime = datetime.datetime.now()
  actualtime = int(actualtime.strftime('%H%M'))
  if(actualtime == heatlight_on):
    requests.get("http://" + ip_shelly3 + "/relay/0?turn=on")
    telegram("Waermespot an")
    sleep(60)
  elif(actualtime == heatlight_off):
    requests.get("http://" + ip_shelly3 + "/relay/0?turn=off")
    telegram("Waermespot aus")
    sleep(60)

###Rain function for Rain at specific times config "raintime" for times to rain and starts 2 min after ventilation
def rain():
  actualtime = datetime.datetime.now()
  actualtime = int(actualtime.strftime('%H%M'))
  z=[raintime1,raintime2,raintime3,raintime4,raintime5,raintime6,raintime7,raintime8,raintime9,raintime10]
  for i in range(0,11):
    if(z[i] == actualtime):
      lcd.clear()
      lcd.printString("       Regen",lcd.LINE_2)
      lcd.printString("     gestartet",lcd.LINE_3)
      my_pwm.ChangeDutyCycle(0)
      requests.get("http://" + ip_shelly1 + "/relay/0?turn=on")
      telegram("Regen gestartet")
      sleep(rainduration)
      lcd.printString("       Regen",lcd.LINE_2)
      lcd.printString("      beendet",lcd.LINE_3)
      requests.get("http://" + ip_shelly1 + "/relay/0?turn=off")
      telegram("Regen beendet")
      sleep(180)
      lcd.printString("     L\xF5ftung",lcd.LINE_2)
      lcd.printString("      gestartet",lcd.LINE_3)
      my_pwm.ChangeDutyCycle(100)
      telegram("Lueftung nach Regen an")
      sleep(300)
      lcd.printString("     L\xF5ftung",lcd.LINE_2)
      lcd.printString("      beendet",lcd.LINE_3)
      my_pwm.ChangeDutyCycle(0)
      telegram("Lueftung nach Regen aus")
      sleep(2)

###Fan temperature control with change dutycycle for specific temperatures
def fan(TempBME280):
  TempBME280=int(TempBME280)
  if(TempBME280 >= 30):
    my_pwm.ChangeDutyCycle(100)
    fanstatus = ("ON 100%")
  elif(TempBME280 >= 29):
    my_pwm.ChangeDutyCycle(75)
    fanstatus = ("ON 75%")
  elif(TempBME280 >= 28):
    my_pwm.ChangeDutyCycle(50)
    fanstatus = ("ON 50%")
  else:
    fanstatus = ("Off 0%")
    my_pwm.ChangeDutyCycle(0)
  return fanstatus

###DS18B20 getting Temperature function
def getTemp_DS18B20(ID):
  file = open(ID)
  rawData = file.read()
  file.close()
  rawValue = rawData.split("\n")[1].split(" ")[9]
  temperature = int(float(rawValue[2:]) / 1000)
  return '%6.2f' % temperature

###Telegram notification
def telegram(msg):
  telegram_msg=msg
  send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + telegram_msg
  response = requests.get(send_text)

#  return response.json()



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
