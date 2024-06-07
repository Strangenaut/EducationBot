from config import *


def send_english_options(message, bot):
    if message.text != SUBJECT_ENGLISH:
        return
    
    bot.send_message(message.chat.id, text='Its English branch', parse_mode='html')