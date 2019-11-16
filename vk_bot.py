import vk_api
import psycopg2
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from classes import VkBot
import random

conn = psycopg2.connect(database="hack", user="postgres", host="100.100.153.231",
                        port="5432", password="verepa40")
cursor = conn.cursor()
keyboard = None


token = '9becfa2210b0bbd028f47951ae253aa88c15fc26c6c938578980bdd472581fcaad29eab2afd0f7109f06f'
vk = vk_api.VkApi(token=token)
vk_mess = vk.get_api()
bot = VkBot(vk_mess)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            bot.new_messages(event.user_id, event.text)
            print('Text: ', event.text)
