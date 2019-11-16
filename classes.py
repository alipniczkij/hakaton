from db import session, User, Message
from bot_neuro import *
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import requests
import json
import bs4


def create_start_keyboard(text):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(text, color=VkKeyboardColor.POSITIVE)
    return keyboard
    # keyboard.add_button('Белая кнопка', color=VkKeyboardColor.DEFAULT)
    # keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

    # keyboard.add_line()  # Переход на вторую строку
    # keyboard.add_button('Белая кнопка', color=VkKeyboardColor.DEFAULT)
    # keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)


class VkBot:
    def __init__(self, vk):
        self.vk = vk
        self.start_keyboard = create_start_keyboard('Регистрация')
        # self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["РЕГИСТРАЦИЯ", "ВАФЛЯ"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    def login_user(self, user_id):
        in_system = session.query(User).filter_by(user_id=user_id).first()
        if in_system:
            self.send_message(user_id=user_id, messages="Введите запрос:")
        else:
            user = User(user_id)
            session.add(user)
            session.commit()
            self.send_message(user_id=user_id, messages="Здравствуйте " + self._get_user_name_from_vk_id(user_id))

    def save_massage(self, user_id, message):
        mes = Message(user_id, message)
        session.add(mes)
        session.commit()

    def new_message(self, user_id, message):

        in_system = session.query(User).filter_by(user_id=user_id).first()
        if not in_system and message.upper() != self._COMMANDS[0] and message.upper() != self._COMMANDS[1]:
            self.send_message(user_id, messages='Требуется регистрация', keyboard=self.start_keyboard)
            return
        self.save_massage(user_id, message)

        if message.upper() == self._COMMANDS[0]:
            if in_system:
              return
            self.send_message(user_id=user_id, messages="Введите кодовое слово")
        elif message.upper() == self._COMMANDS[1]:
            self.login_user(user_id)
            self.send_message(messages='Введите запрос:', user_id=user_id)
        else:
            answer = classify(message)
            self.send_message(messages='Класс - ' + str(answer[0]), user_id=user_id)
            self.send_message(messages='Введите запрос:', user_id=user_id)

    def send_message(self, user_id, messages='', keyboard=None):
        if keyboard:
            self.vk.messages.send(
                peer_id=user_id,
                random_id=get_random_id(),
                keyboard=json.dumps(keyboard.keyboard),
                message=messages
            )
        else:
            self.vk.messages.send(
                peer_id=user_id,
                random_id=get_random_id(),
                message=messages
            )
