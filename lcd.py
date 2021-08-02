"""
16x2 I2C Display
Version 1.0.0
DELOARTS Research Inc.
Philip Delorenzo
02.05.2016
"""
import smbus
from time import sleep
#################################################################################################
##### CONSTANTS AND ADDRESSES ###################################################################
#################################################################################################
# Basic display data (change them for your display)
ADDR  = 0x27 # I2C device address
WIDTH = 20   # Maximum characters per line
# Device constants
CHR = 1 # Mode - Sending data
CMD = 0 # Mode - Sending command
# Device addresses (refer to the data sheet)
LINE_1 = 0x80
LINE_2 = 0xC0
LINE_3 = 0x94
LINE_4 = 0xD4
BACKLIGHT = 0x08
NO_BACKLIGHT = 0x00
INITIALIZE1 = 0x33
INITIALIZE2 = 0x32
INITIALIZE3 = 0x0C
CURSORMVDIR = 0x06
DATALENGHT = 0x2B
CLEAR = 0x01
# The enable bit for the display
ENABLE = 0b00000100
# Time "delays" for the I2C bus
E_PULSE = 0.0005
E_DELAY = 0.0005
# Enable the I2C bus
i2c = smbus.SMBus(1) # Rev 2 Pi uses 1
#################################################################################################
##### INITIALIZE THE DISPLAY ####################################################################
#################################################################################################
def initialize():
  sendByte(INITIALIZE1, CMD)
  sendByte(INITIALIZE2, CMD)
  sendByte(CURSORMVDIR, CMD)
  sendByte(INITIALIZE3, CMD)
  sendByte(DATALENGHT, CMD)
  sleep(E_DELAY)
  clear()
  backlight()
#################################################################################################
##### SEND BYTES ################################################################################
#################################################################################################
def sendByte(bits, mode):
  # bits = data
  # mode = 1 for data
  #        0 for command
  bitsHigh = mode | (bits & 0xF0) | BACKLIGHT
  bitsLow = mode | ((bits<<4) & 0xF0) | BACKLIGHT

  i2c.write_byte(ADDR, bitsHigh)
  sleep(E_DELAY)
  i2c.write_byte(ADDR, (bitsHigh | ENABLE))
  sleep(E_PULSE)
  i2c.write_byte(ADDR,(bitsHigh & ~ENABLE))
  sleep(E_DELAY)
  i2c.write_byte(ADDR, bitsLow)
  sleep(E_DELAY)
  i2c.write_byte(ADDR, (bitsLow | ENABLE))
  sleep(E_PULSE)
  i2c.write_byte(ADDR,(bitsLow & ~ENABLE))
  sleep(E_DELAY)
#################################################################################################
##### ENABLE / DISABLE BACKLIGHT ################################################################
#################################################################################################
def backlight():
  i2c.write_byte(ADDR, BACKLIGHT)
def noBacklight():
  i2c.write_byte(ADDR, NO_BACKLIGHT)
#################################################################################################
##### CLEAR THE DISPLAY #########################################################################
#################################################################################################
def clear():
  sendByte(CLEAR, CMD)
#################################################################################################
##### PRINT A STRING ON THE DISPLAY #############################################################
#################################################################################################
def printString(message, line):
  message = message.ljust(WIDTH, " ")
  sendByte(line, CMD)
  for i in range(WIDTH):
    sendByte(ord(message[i]), CHR)
#################################################################################################
##### MAIN ######################################################################################
#################################################################################################
if __name__ == "__main__":
  initialize()
  printString("    DELOARTS    ", LINE_1)
  printString(" 16x2/4 I2C LCD ", LINE_2)
#################################################################################################
##### END OF CODE ###############################################################################
#################################################################################################
