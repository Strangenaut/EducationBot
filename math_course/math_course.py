import os
from config import *
from math_course.config import *
from util.load_files import load_files


math_data_path = os.path.join(PROJECT_ROOT_PATH, 'math_course', 'data')
def send_math_options(message, bot):
    bot.send_message(message.chat.id, MATH_TRAINING_MATERIALS)
    media = load_files(math_data_path)
    bot.send_media_group(message.chat.id, media)