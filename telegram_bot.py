from telegram.ext import Application, MessageHandler, CommandHandler, filters
from dialogflow_api import detect_intent_texts


async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text("Привет! Я бот, подключенный к Dialogflow. Напиши мне что-нибудь!")


async def handle_message(update, context):
    """Обрабатываем входящие текстовые сообщения"""
    if not update.message or not update.message.text:  # Игнорируем пустые сообщения
        return

    text = update.message.text  # Получаем текст сообщения пользователя
    chat_id = update.effective_user.id  # Получаем ID чата пользователя

    # Вызываем Dialogflow API
    response = detect_intent_texts('denis-lxju', chat_id, [text], 'RU-ru')

    # Отправляем ответ от Dialogflow пользователю
    await update.message.reply_text(response)


def main():
    TOKEN = "7808382160:AAHRd-iVztS4eVchkwbITXjp9o0QG3sJf2o"  # Ваш токен бота от BotFather

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))  # Команда /start

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()