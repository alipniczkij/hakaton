import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from classes import VkBot
import random


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})


token = '9becfa2210b0bbd028f47951ae253aa88c15fc26c6c938578980bdd472581fcaad29eab2afd0f7109f06f'


vk = vk_api.VkApi(token=token)


longpoll = VkLongPoll(vk)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            print('New message:')
            print(f'For me by: {event.user_id}', end='')

            bot = VkBot(event.user_id)
            write_msg(event.user_id, bot.new_message(event.text))

            print('Text: ', event.text)
