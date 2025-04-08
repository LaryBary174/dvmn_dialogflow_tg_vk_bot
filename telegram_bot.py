import time
import requests
import telegram
from environs import Env
from telegram.ext import Updater, MessageHandler, Filters,CallbackContext
from functools import partial
from bot_for_logging import get_logger
from dialogflow_api import detect_intent_texts


def handle_message(update, context: CallbackContext, project_id: str):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    chat_id = update.effective_user.id
    response = detect_intent_texts(project_id, chat_id, [text], 'RU-ru')


    update.message.reply_text(response)


def main():
    env = Env()
    env.read_env()
    bot_token = env.str("TELEGRAM_BOT_TOKEN")
    logger_bot_token = env.str("TG_LOG_TOKEN")
    logger_chat_id = env.str("TELEGRAM_CHAT_ID")
    project_id = env.str('GOOGLE_PROJECT_ID')
    logger_bot = telegram.Bot(token=logger_bot_token)
    logger = get_logger(logger_bot, logger_chat_id)
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher


    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, partial(handle_message, project_id=project_id))
    )


    while True:
        try:
            logger.info("Бот запущен...")
            updater.start_polling()
            updater.idle()
        except requests.exceptions.ReadTimeout:
            logger.warning('Повтор запроса')

            continue
        except requests.exceptions.ConnectionError:
            logger.error('Ошибка соединения, повторная попытка через 10 секунд')


            time.sleep(10)
        except telegram.error.TelegramError:
            logger.error('Ошибка Телеграмм, повторная попытка через 10 секунд')

            time.sleep(10)
        except telegram.error.NetworkError:
            logger.error('Ошибка подключения, повторная попытка через 10 сек')

            time.sleep(10)

if __name__ == "__main__":
    main()
