import os
import pandas as pd
import random
from util.dict_slice import dict_slice
from telebot import types
from config import *
from english_course.config import *
from util.load_files import load_files


english_options_descriptions = [
    ENGLISH_TRAINING_MATERIALS,
    WORDS_TEST,
    ENGLISH_USEFUL_LINKS,
    BACK
]
english_data_path = os.path.join(PROJECT_ROOT_PATH, 'english_course', 'data', 'materials')
min_index = None
max_index = None
last_word = None

def send_english_options(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for description in english_options_descriptions:
        markup.add(types.KeyboardButton(description))

    bot.send_message(
        message.chat.id, 
        text=MAKE_CHOICE, 
        parse_mode='html', 
        reply_markup=markup
    )

def send_english_training_materials(message, bot):
    bot.send_message(message.chat.id, TAKE_ENGLISH_MATERIALS)
    media = load_files(english_data_path)
    bot.send_media_group(message.chat.id, media)

def load_words():
    words_file_path = os.path.join(PROJECT_ROOT_PATH, 'english_course', 'data', 'Words.csv')
    df = pd.read_csv(words_file_path)
    return dict(zip(df.Eng, df.Rus))

def send_word_test_explanation(message, bot):
    bot.send_message(
        message.chat.id, 
        WORDS_TEST_EXPLANATION.format(len(words)), 
        parse_mode='html'
    )

def send_word_question(message, bot):
    global last_word, current_words_dict, min_index, max_index

    if not current_words_dict:
        current_words_dict = dict_slice(words, min_index, max_index)

    text = message.text.replace(' ', '')
    if text.replace('-', '').isnumeric():
        indices = text.split('-')
        min_index = int(indices[0]) - 1
        max_index = int(indices[1]) - 1
        current_words_dict = dict_slice(current_words_dict, min_index, max_index)

    if message.text == FORGOT and last_word != None:
        bot.send_message(message.chat.id, text='Перевод: ' + words[last_word])
    
    i = random.randint(0, len(current_words_dict) - 1)
    key = list(current_words_dict.keys())[i]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_row = [
        types.KeyboardButton(REMEMBER),
        types.KeyboardButton(FORGOT),
        types.KeyboardButton(BACK)
    ]
    markup.add(*buttons_row)

    bot.send_message(message.chat.id, text=key, reply_markup=markup)
    last_word = key
    del current_words_dict[key]

def send_english_useful_links(message, bot):
    bot.send_message(message.chat.id, text=ENGLISH_LINKS, disable_web_page_preview=True)

words = load_words()
current_words_dict = words.copy()