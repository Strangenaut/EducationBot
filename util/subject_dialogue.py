from config import *
from telebot import types
from util.load_files import load_files


class SubjectDialogue:
    def __init__(self, bot, materials_path, options_descriptions, text_reply_scenarios, links_path):
        self.bot = bot
        self.materials_path = materials_path
        self.options_descriptions = options_descriptions
        self.text_reply_scenarios = text_reply_scenarios
        self.links_path = links_path

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

    def __delete_txt_files(self, files_list):
        documents = list(
            filter(
                lambda x: 
                    not x.media.file_name.endswith('.txt'),
                    files_list
                )
            )
        return documents

    def send_training_materials(self, message, no_txt=True):
        if not os.path.exists(self.materials_path):
            self.bot.send_message(message.chat.id, NO_MATERIALS)
            return

        self.bot.send_message(message.chat.id, TAKE_MATERIALS)
        media = load_files(self.materials_path)

        if no_txt:
            media = self.__delete_txt_files(media)

        self.bot.send_media_group(message.chat.id, media) 

    def send_useful_links(self, message):
        if not os.path.exists(self.links_path):
            self.bot.send_message(message.chat.id, NO_LINKS)
            return
        
        with open(self.links_path, 'r', encoding='utf-8') as file:
            self.bot.send_message(
                message.chat.id, 
                text=file.read(), 
                disable_web_page_preview=True
                )

    def send_links_adding_explanation(self, message):
        self.bot.send_message(message.chat.id, text=LINKS_ADDING_EXPLANATION)
    
    def send_materials_adding_explanation(self, message):
        self.bot.send_message(message.chat.id, text=MATERIALS_ADDING_EXPLANATION)
    
    def add_links(self, links_path, links_to_add):
        with open(links_path, 'w') as file:
            file.write('\n' + links_to_add)

    def add_documents(self, documents_path, document_to_add):
        with open(documents_path, 'wb') as f:
            f.write(document_to_add.read())
    
    def add_materials(self):
        pass