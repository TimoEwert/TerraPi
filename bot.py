#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
import configparser

###Edit config file (.env) to change parameters
config = configparser.ConfigParser()
config.read("/home/pi/TerraPi/.env2")

bot_token=config["Configuration"]["bot_token"] ###token for Telegram Bot
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('0%', '25%', '50%', '75%', '100%')
    keyboard.row('Automatik')
    keyboard.row('Status')
    bot.send_message(message.chat.id, 'Lüftersteuerung', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_text(message):
    drehzahl = message.text.lower()
    try:
        if drehzahl=="status":
            file = open("/home/pi/TerraPi/status.tmp", "r")
            status=file.read()
            file.close()
            bot.send_message(message.chat.id, status)
        if drehzahl=="0%" or drehzahl=="25%" or drehzahl=="50%" or drehzahl=="75%" or drehzahl=="100%" or drehzahl=="automatik":
            bot.send_message(message.chat.id, 'Setze Lüfter auf ' + drehzahl)
            drehzahl=drehzahl.replace('%', '')
            file = open("/home/pi/TerraPi/dutycycle.tmp","w")
            file.write(drehzahl)
            file.close()
    except:
        print("Fehler")
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
#bot.polling()
