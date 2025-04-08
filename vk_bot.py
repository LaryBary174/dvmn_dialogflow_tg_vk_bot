
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow_api import detect_intent_texts

def vk_bot_with_dialogflow(event, vk_api,):
    response = detect_intent_texts('denis-lxju', event.user_id, [event.text], 'RU-ru')
    vk_api.messages.send(
        user_id=event.user_id,
        message=response,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token="vk1.a.aCaP05waL4YjUtKsAhndjT_iC5Yfl6EY7Z2o67z6OQvKrFYkZhLsJdG9j36ViuNBe-ZsAuii7ebeiiIMbeucNWy4sBTL9m2ZcG12f8CsjJtSrXe1Yp5f7kbK9r7sUn-yxG5J7Pw1C6NTI7J1ldBgTO4-vU8mBCjXlqzOPpbw-OCvZCicaD2W7MQsDyTkAOSjx69mN5OzWC3WlpwcinmEjA")
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            vk_bot_with_dialogflow(event, vk_api)