import os
import telebot
from telebot import types
from english_course.english_course import *
from math_course.math_course import *
from config import *
from english_course.config import *
from math_course.config import *
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
text_reply_scenarios = {
    SUBJECT_ENGLISH: send_english_options,
    SUBJECT_MATH: send_math_options,
    ENGLISH_TRAINING_MATERIALS: send_english_training_materials,
    WORDS_TEST: send_word_test_explanation,
    REMEMBER: send_word_question,
    FORGOT: send_word_question,
    ENGLISH_USEFUL_LINKS: send_english_useful_links
}

@bot.message_handler(commands=['start'])
def start_bot(message):    
    markup = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True)
    buttons_row = [
        types.KeyboardButton(SUBJECT_ENGLISH), 
        types.KeyboardButton(SUBJECT_MATH)
    ]
    markup.add(*buttons_row)
    
    bot.send_message(message.chat.id, WELCOME_MESSAGE, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_reply_to_text(message):
    if message.text == BACK:
        start_bot(message)
        return

    if message.text.replace(' ', '').replace('-', '').isnumeric():
        send_word_question(message, bot)
        return

    text_reply_scenarios[message.text](message, bot)


bot.infinity_polling()