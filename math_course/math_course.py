import os
from config import *
from math_course.config import *
from util.load_files import load_files
from util.subject_dialogue import SubjectDialogue


class MathSubjectDialogue(SubjectDialogue):
    def __init__(self, bot):
        materials_path = os.path.join(PROJECT_ROOT_PATH, 'math_course', 'data')
        options_descriptions = [
            DIFF_EQUATIONS,
            LINAL,
            MATH_AN,
            PREVIOUS_TASKS_EXAMPLES,
            PROB_THEORY,
            STATS,
            BACK
        ]

        super().__init__(
            bot=bot, 
            materials_path=materials_path, 
            options_descriptions=options_descriptions, 
            text_reply_scenarios=None, 
            links=None
        )
        self.translation_dict = {
            subject_name: subject_name_translation 
            for subject_name, subject_name_translation 
            in zip(options_descriptions[:-1], os.listdir(materials_path))
        }

    def send(self, message):
        if message.text == SUBJECT_MATH:
            self.send_options(message)
            return
        
        self.send_training_materials(message)

    def send_training_materials(self, message):
        subject_name = self.translation_dict[message.text]
        subject_path = os.path.join(self.materials_path, subject_name)
        media = load_files(subject_path)

        documents = list(
            filter(
                lambda x: 
                    not x.media.file_name.endswith('.txt'),
                    media
                )
            )
        self.bot.send_media_group(
                message.chat.id,
                documents
        )
        links_path = os.path.join(subject_path, f'{LINKS_FILE_NAME}.txt')

        if not os.path.exists(links_path):
            return

        with open(links_path, 'r') as file:
            self.links = file.read()

        self.send_useful_links(message)