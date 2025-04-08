import requests
import time
import telegram
import random
from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from bot_for_logging import get_logger
from dialogflow_api import detect_intent_texts

def vk_bot_with_dialogflow(event, vk_api, project_id: str):
    response = detect_intent_texts(project_id, event.user_id, [event.text], 'RU-ru')
    vk_api.messages.send(
        user_id=event.user_id,
        message=response,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    env.read_env()
    vk_token = env.str("VK_GROUP_API_KEY")
    project_id = env.str('GOOGLE_PROJECT_ID')
    logger_bot_token = env.str("TG_LOG_TOKEN")
    logger_chat_id = env.str("TELEGRAM_CHAT_ID")
    logger_bot = telegram.Bot(token=logger_bot_token)
    logger = get_logger(logger_bot, logger_chat_id)
    vk_session = vk.VkApi(token=vk_token)
    while True:
        try:
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            logger.info('VK бот запущен!')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    vk_bot_with_dialogflow(event, vk_api, project_id)
        except requests.exceptions.ReadTimeout:
            logger.warning('Повтор запроса')
            continue
        except requests.exceptions.ConnectionError:
            logger.error('Ошибка соединения, повторная попытка через 10 секунд')
            time.sleep(10)

        except vk.exceptions.ApiError:
            logger.error('Ошибка API VK !')

if __name__ == "__main__":
    main()