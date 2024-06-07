import os
import telebot
from telebot import types
from english_course.english_subject_dialogue import EnglishSubjectDialogue
from math_course.math_course import *
from config import *
from english_course.config import *
from math_course.config import *
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))
subject_dialogs = {
    SUBJECT_ENGLISH: EnglishSubjectDialogue(bot=bot),
    SUBJECT_MATH: None
}
current_subject_dialogue = None

@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True)
    buttons_row = [
        types.KeyboardButton(SUBJECT_ENGLISH), 
        types.KeyboardButton(SUBJECT_MATH)
    ]
    markup.add(*buttons_row)
    
    bot.send_message(message.chat.id, WELCOME_MESSAGE, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_reply_to_text(message):
    global current_subject_dialogue
    
    if message.text == BACK:
        current_subject_dialogue = None
        start_bot(message)
        return

    if current_subject_dialogue is None:
        current_subject_dialogue = subject_dialogs[message.text]

    current_subject_dialogue.send(message)


bot.infinity_polling()