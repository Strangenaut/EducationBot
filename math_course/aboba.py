import os
from telebot import types


path = os.path.dirname(__file__)
path = os.path.join(path, 'data', 'Linalg', 'links.txt')


a = types.InputMediaDocument(media=types.InputFile(path))
b = a.media
print(b.file_name)
print(isinstance(types.InputMediaDocument(media=types.InputFile(path)), str))

print(types.InputMediaDocument(media=types.InputFile(path)))