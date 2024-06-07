import os
from telebot import types


def load_files(files_path):
    files_list = os.listdir(files_path)
    media = []

    for file_name in files_list:
        file_path = os.path.join(files_path, file_name)

        if str(file_name).endswith('.txt'):
            with open(file_path) as file:
                media.append(file.read())
            continue
        media.append(types.InputMediaDocument(media=types.InputFile(file_path)))
    
    return media