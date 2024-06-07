import os
import telebot
from telebot import types
from english import send_english_options
from config import *
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
text_reply_scenarios = {
    SUBJECT_ENGLISH: send_english_options
}

@bot.message_handler(commands=['start'])
def start_bot(message):    
    markup = types.ReplyKeyboardMarkup()
    button_english = types.KeyboardButton(SUBJECT_ENGLISH)
    button_math = types.KeyboardButton(SUBJECT_MATH)
    markup.add(button_english)
    markup.add(button_math)
    bot.send_message(message.chat.id, WELCOME_MESSAGE, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_reply_to_text(message):
    text_reply_scenarios[message.text](message, bot)

bot.infinity_polling()