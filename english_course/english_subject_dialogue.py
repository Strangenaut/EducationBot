import os
import pandas as pd
import random
from telebot import types
from util.dict_slice import dict_slice
from core.subject_dialogue import SubjectDialogue
from config import *
from english_course.config import *


class EnglishSubjectDialogue(SubjectDialogue):
    def __init__(self, bot):
        materials_path = os.path.join(PROJECT_ROOT_PATH, 'english_course', 'data', 'materials')
        options_descriptions = [
            ENGLISH_TRAINING_MATERIALS,
            WORDS_TEST,
            ENGLISH_USEFUL_LINKS,
            BACK
        ]
        text_reply_scenarios = {
            SUBJECT_ENGLISH: self.send_options,
            ENGLISH_TRAINING_MATERIALS: self.send_training_materials,
            ENGLISH_USEFUL_LINKS: self.send_useful_links,
            WORDS_TEST: self.send_word_test_explanation,
            REMEMBER: self.send_word_question,
            FORGOT: self.send_word_question,
            LINKS: self.send_links_adding_explanation,
            MATERIALS: self.send_materials_adding_explanation
        }
        links_path = os.path.join(materials_path, 'links.txt')
        super().__init__(
            bot=bot, 
            materials_path=materials_path,
            options_descriptions=options_descriptions,
            text_reply_scenarios=text_reply_scenarios,
            links_path=links_path
        )

        self.all_words = self.load_words()
        self.current_words_dict = self.all_words.copy()
        self.min_index = None
        self.max_index = None
        self.last_word = None
    
    def send(self, message):
        text = message.text.replace(' ', '')

        if text.replace('-', '').isnumeric():
            indices = message.text.split('-')
            self.min_index = int(indices[0]) - 1
            self.max_index = int(indices[1]) - 1
            self.current_words_dict = dict_slice(
                self.all_words,
                self.min_index,
                self.max_index
            )
            self.send_word_question(message)
            return
        
        super().send(message)

    def send_word_test_explanation(self, message):
        self.bot.send_message(
            message.chat.id, 
            WORDS_TEST_EXPLANATION.format(len(self.all_words))
        )
    
    def send_word_question(self, message):
        if not self.current_words_dict:
            self.current_words_dict = dict_slice(self.all_words, self.min_index, self.max_index)

        if message.text == FORGOT and self.last_word != None:
            self.bot.send_message(
                message.chat.id, 
                text='Перевод: ' + self.all_words[self.last_word]
            )
        
        key = random.choice(list(self.current_words_dict.keys()))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons_descriptions = [
            REMEMBER,
            FORGOT,
            BACK
        ]
        markup.add(*list(map(types.KeyboardButton, buttons_descriptions)))

        self.bot.send_message(message.chat.id, text=key, reply_markup=markup)
        self.last_word = key
        del self.current_words_dict[key]

    def load_words(self):
        words_file_path = os.path.join(PROJECT_ROOT_PATH, 'english_course', 'data', 'Words.csv')
        df = pd.read_csv(words_file_path)
        return dict(zip(df.Eng, df.Rus))