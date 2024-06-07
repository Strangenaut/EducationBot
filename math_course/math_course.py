from config import *
import os
from telebot import types


math_data_path = os.path.join(PROJECT_ROOT_PATH, 'math_course', 'data')
def send_math_options(message, bot):
    if message.text != SUBJECT_MATH:
        return
    
    files_list = os.listdir(math_data_path)
    media = []

    for file_name in files_list:
        file_path = os.path.join(math_data_path, file_name)
        media.append(types.InputMediaDocument(media=types.InputFile(file_path)))

    bot.send_message(message.chat.id, 'Вот все материалы по математике:')

    bot.send_media_group(message.chat.id, media)

    