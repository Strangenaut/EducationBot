import os
import telebot
from telebot import types
from config import WELCOME_MESSAGE
from dotenv import load_dotenv

load_dotenv()

botTimeWeb = telebot.TeleBot(os.getenv('TOKEN'))

@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = WELCOME_MESSAGE
    
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text = 'Да', callback_data='Да')
    markup.add(button_yes)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

botTimeWeb.infinity_polling()