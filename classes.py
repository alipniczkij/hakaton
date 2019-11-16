import requests
import bs4


def create_start_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Регистрация', color=VkKeyboardColor.POSITIVE)
    return keyboard
    # keyboard.add_button('Белая кнопка', color=VkKeyboardColor.DEFAULT)
    # keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

    # keyboard.add_line()  # Переход на вторую строку
    # keyboard.add_button('Белая кнопка', color=VkKeyboardColor.DEFAULT)
    # keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)


class VkBot:
    def __init__(self, vk):
        self.vk = vk
        self.start_keyboard = create_start_keyboard()
        self._USERNAME = self._get_user_name_from_vk_id(user_id)
        self._COMMANDS = ["РЕГИСТРАЦИЯ"]

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

    def new_message(self, user_id, message):
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"
        else:
            return "Не понимаю о чем вы..."

    def send_message(self, user_id, messages='', keyboard=None):
        self_vk.messages.send(
            peer_id=user_id,
            random_id=get_random_id(),
            keyboard=keyboard,
            message=messages
        )
