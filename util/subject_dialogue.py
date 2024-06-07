from config import *
from telebot import types
from util.load_files import load_files


class SubjectDialogue:
    def __init__(self, bot, materials_path, options_descriptions, text_reply_scenarios, links):
        self.bot = bot
        self.materials_path = materials_path
        self.options_descriptions = options_descriptions
        self.text_reply_scenarios = text_reply_scenarios
        self.links = links

    def send(self, message):
        self.text_reply_scenarios[message.text](message)

    def send_options(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for description in self.options_descriptions:
            markup.add(types.KeyboardButton(description))

        self.bot.send_message(
            message.chat.id, 
            text=MAKE_CHOICE, 
            parse_mode='html', 
            reply_markup=markup
        )

    def send_training_materials(self, message):
        self.bot.send_message(message.chat.id, TAKE_MATERIALS)
        media = load_files(self.materials_path)
        self.bot.send_media_group(message.chat.id, media) 

    def send_useful_links(self, message):
        self.bot.send_message(message.chat.id, text=self.links, disable_web_page_preview=True)