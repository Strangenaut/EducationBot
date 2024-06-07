import os
from telebot import types


def load_files(files_path):
    files_list = os.listdir(files_path)
    media = []

    for file_name in files_list:
        file_path = os.path.join(files_path, file_name)
        media.append(types.InputMediaDocument(media=types.InputFile(file_path)))
    
    return media