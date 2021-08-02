# -*- coding: iso-8859-1 -*-
import RPi.GPIO as GPIO
import time
import lcd
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
red=12
GPIO.setup(red,GPIO.OUT)
my_pwm=GPIO.PWM(red,100)
my_pwm.start(0)
humi = True
while humi:
    try:
        humidata = open("/home/pi/terrapi/BME280_humidity_data.txt","r")
        humidity = float(humidata.read())
        if(humidity >= 90):
            my_pwm.ChangeDutyCycle(100)
            fanstatus = ("ON 100%")
            file = open("/home/pi/terrapi/fanstatus.txt","w")
            file.write(fanstatus)
            file.close()
            time.sleep(5)
            print(">= 90 100%")
        elif(humidity >= 80):
            my_pwm.ChangeDutyCycle(75)
            fanstatus = ("ON 75%")
            file = open("/home/pi/terrapi/fanstatus.txt","w")
            file.write(fanstatus)
            file.close()
            time.sleep(5)
            print(">= 80 75%")
        elif(humidity >= 75):
            my_pwm.ChangeDutyCycle(50)
            fanstatus = ("ON 50%")
            file = open("/home/pi/terrapi/fanstatus.txt","w")
            file.write(fanstatus)
            file.close()
            time.sleep(5)
            print(">= 75 50%")
        elif(humidity >= 70):
            my_pwm.ChangeDutyCycle(30)
            fanstatus = ("ON 30%")
            file = open("/home/pi/terrapi/fanstatus.txt","w")
            file.write(fanstatus)
            file.close()
            time.sleep(5)
            print(">= 70 30%")
        elif(humidity < 70):
            my_pwm.ChangeDutyCycle(0)
            fanstatus = ("Off 0%")
            file = open("/home/pi/terrapi/fanstatus.txt","w")
            file.write(fanstatus)
            file.close()
            time.sleep(5)
            print("<70 0%")
        else:
            fanstatus = ("Off 0%")
            file = open("/home/pi/terrapi/fanstatus.txt","w")
            file.write(fanstatus)
            file.close()
            print("else")
            time.sleep(5)
            my_pwm.stop()
            GPIO.cleanup()
            sntemp= False
    except:
        print("Datei wird grad beschrieben. Vorgang übersprungen")
