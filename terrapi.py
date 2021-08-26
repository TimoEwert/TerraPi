#!/usr/bin/python
# -*- coding: utf-8 -*-
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

status1=int(config["Configuration"]["status1"])
status2=int(config["Configuration"]["status2"])
status3=int(config["Configuration"]["status3"])
status4=int(config["Configuration"]["status4"])
status5=int(config["Configuration"]["status5"])
status6=int(config["Configuration"]["status6"])
status7=int(config["Configuration"]["status7"])
status8=int(config["Configuration"]["status8"])
status9=int(config["Configuration"]["status9"])
status10=int(config["Configuration"]["status10"])

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
  temps_humidity()
  mainlight_timer()
  heating_spot_timer()
  tempDS18B20=getTemp_DS18B20(device)
  HumidityBME280="%0.0f" % bme280.relative_humidity
  TempBME280="%0.0f" % bme280.temperature
  fanstatus=fan(TempBME280)
  try:
    lcd.printString("W\xE1rme Spot: " + tempDS18B20 + chr(223) + "C", lcd.LINE_1)
  except:
    print("lcd error")
  lcd.printString("L\xF5fter: " + fanstatus,lcd.LINE_2)
  lcd.printString("Temperatur: " + TempBME280 + chr(223) + "C", lcd.LINE_3)
  lcd.printString("Luftfeucht.:" + HumidityBME280 + "%", lcd.LINE_4)
  sleep(1)

###Lightning timer for shelly2 Main Light
def mainlight_timer():
  actualtime = datetime.datetime.now()
  actualtime = int(actualtime.strftime('%H%M'))
  if(actualtime == mainlight_on):
    try:
      r=requests.get("http://" + ip_shelly2 + "/relay/0?turn=on")
      if(r.status_code == 200):
        telegram("Arcardia LED an")
      else:
        print("Arcardia LED wurde nicht angeschaltet")
      sleep(60)
    except:
      telegram("Arcardia LED wurde nicht angeschaltet")
      sleep(60)

  elif(actualtime == mainlight_off):
    try:
      r=requests.get("http://" + ip_shelly2 + "/relay/0?turn=off")
      if(r.status_code == 200):
        telegram("Arcardia LED aus")
      else:
        print("Arcardia LED wurde nicht ausgeschaltet") 
      sleep(60)
    except:
      telegram("Arcardia LED wurde nicht ausgeschaltet")
      sleep(60)
###Lightning timer for shelly3 Heating Spot
def heating_spot_timer():
  actualtime = datetime.datetime.now()
  actualtime = int(actualtime.strftime('%H%M'))
  if(actualtime == heatlight_on):
    try:
      r=requests.get("http://" + ip_shelly3 + "/relay/0?turn=on")
      if(r.status_code == 200):
        telegram("Wärmespot an")
      else:
        print("Wärmespot wurde nicht angeschaltet")
      sleep(60)
    except:
      telegram("Wärmespot wurde nicht angeschaltet")
      sleep(60)

  elif(actualtime == heatlight_off):
    try:
      r=requests.get("http://" + ip_shelly3 + "/relay/0?turn=off")
      if(r.status_code == 200):
        telegram("Wärmespot aus")
      else:
        print("Wärmespot wurde nicht ausgeschaltet") 
      sleep(60)
    except:
      telegram("Wärmespot wurde nicht ausgeschaltet")
      sleep(60)
###Rain function for Rain at specific times config "raintime" for times to rain and starts 2 min after ventilation
def rain():
  actualtime = datetime.datetime.now()
  actualtime = int(actualtime.strftime('%H%M'))
  raintimes=[raintime1,raintime2,raintime3,raintime4,raintime5,raintime6,raintime7,raintime8,raintime9,raintime10]
  for i in range(10):
    if(raintimes[i] == actualtime):
      lcd.clear()
      lcd.printString("       Regen",lcd.LINE_2)
      lcd.printString("     gestartet",lcd.LINE_3)
      my_pwm.ChangeDutyCycle(0)
      try:
        r=requests.get("http://" + ip_shelly1 + "/relay/0?turn=on")
        if(r.status_code == 200):
          telegram("Regen gestartet")
        else:
          print("Regen wurde nicht gestartet")
      except:
        telegram("Regen wurde nicht gestartet")
      sleep(rainduration)
      lcd.printString("       Regen",lcd.LINE_2)
      lcd.printString("      beendet",lcd.LINE_3)
      try:
        r=requests.get("http://" + ip_shelly1 + "/relay/0?turn=off")
        if(r.status_code == 200):
          telegram("Regen beendet")
        else:
          print("Regen wurde nicht beendet")
      except:
        telegram("Regen wurde nicht beendet")
      sleep(180)
      lcd.printString("    L\xF5ftung",lcd.LINE_2)
      lcd.printString("       gestartet",lcd.LINE_3)
      my_pwm.ChangeDutyCycle(100)
      telegram("Lüftung nach Regen an")
      sleep(180)
      lcd.printString("     L\xF5ftung",lcd.LINE_2)
      lcd.printString("        beendet",lcd.LINE_3)
      my_pwm.ChangeDutyCycle(0)
      telegram("Lüftung nach Regen aus")
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
  try:
    file = open(ID)
    rawData = file.read()
    file.close()
    rawValue = rawData.split("\n")[1].split(" ")[9]
    temperature = int(float(rawValue[2:]) / 1000)
    return '%6.2f' % temperature
  except:
    actualtime = datetime.datetime.now()
    actualtime = actualtime.strftime('%H:%M:%S')
    telegram(actualtime + " Fehler in der Erfassung des Wertes vom DS18B20")
    sleep(5)
    
###Telegram notification
def telegram(msg):
  telegram_msg=msg
  send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + telegram_msg
  response = requests.get(send_text)

###sends temps, humidiy and fan status to telegram
def temps_humidity():
  actualtime = datetime.datetime.now()
  actualtime = int(actualtime.strftime('%H%M'))
  status=[status1,status2,status3,status4,status5,status6,status7,status8,status9,status10]
  for i in range(10):
    if(status[i] == actualtime):
      tempDS18B20=getTemp_DS18B20(device)
      TempBME280="%0.0f" % bme280.temperature
      HumidityBME280="%0.0f" % bme280.relative_humidity
      telegram("Wärmespot: " + tempDS18B20 + "°C \n" + "Temperatur: " +  TempBME280 + "°C \n" + "Luftfeuchtigkeit: " + HumidityBME280 + "%")
      sleep(60)
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
