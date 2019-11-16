import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from classes import VkBot
import random
import socket
from multiprocessing import Process, Value
from time import time, sleep
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)

token = '9becfa2210b0bbd028f47951ae253aa88c15fc26c6c938578980bdd472581fcaad29eab2afd0f7109f06f'
vk = vk_api.VkApi(token=token)
vk_mess = vk.get_api()
bot = VkBot(vk_mess)
longpoll = VkLongPoll(vk)


def listen(metric):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                bot.new_message(event.user_id, event.text)
                metric.value += 1

def send(metric):
   while True:
       s = socket.create_connection(('35.204.44.141', 2003))
       s.sendall(f'hackathon.team2.backend.cnt {metric.value} -1\n'.encode('utf-8'))
       print(metric.value)
       metric.value = 0
       sleep(60)


metric = Value('i', 0)
fr = Process(target=listen, args=(metric, ))
sc = Process(target=send, args=(metric, ))
fr.start()
sc.start()
