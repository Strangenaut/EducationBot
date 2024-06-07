import os
import telebot
from telebot import types
from config import *
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def startBot(message):    
    markup = types.ReplyKeyboardMarkup()
    button_english = types.KeyboardButton(SUBJECT_ENGLISH)
    button_math = types.KeyboardButton(SUBJECT_MATH)
    markup.add(button_english)
    markup.add(button_math)
    bot.send_message(message.chat.id, WELCOME_MESSAGE, parse_mode='html', reply_markup=markup)

bot.infinity_polling()