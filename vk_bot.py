import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from classes import VkBot
import random


from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

token = '9becfa2210b0bbd028f47951ae253aa88c15fc26c6c938578980bdd472581fcaad29eab2afd0f7109f06f'
vk = vk_api.VkApi(token=token)
vk_mess = vk.get_api()
bot = VkBot(vk_mess)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            bot.new_message(event.user_id, event.text)
            print('Text: ', event.text)
