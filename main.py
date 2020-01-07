import vk_api, requests, bs4
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from messages import vkbot
from function import Afisha

def msg(user_id, Message):
    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = Message)    
    
vk_sess = vk_api.VkApi(token = "3065c03cd80efe01b7caf2d5c650ccf219e73c8a54728cb9af85091c27fda9a2d8b599f2ea72ad35d475c")
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)

for event in longpoll.listen():
    print(event)
    #boolean1 = boolean2 = False

    if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me and event.from_user:
        bot = vkbot(event.user_id)
        text = event.text
        print(text)
        mess = bot.new_msg(text)
        for j in mess:
            try: 
                msg(event.user_id, j)
            except: 
                msg(event.user_id, 'По вашему запросу ничего не найдено')