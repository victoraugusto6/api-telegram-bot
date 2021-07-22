import telegram
from decouple import config
from telegram.ext import CommandHandler, Updater
import requests

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
DEBUG = config('DEBUG')
APP_NAME_HEROKU = config('APP_NAME_HEROKU')


def foto_gatos(update, context):
    message = f'Olá, {update.message.from_user.first_name}! 😎\n'
    message += 'Olha o gatinho:'

    response = requests.get('https://thatcopy.pw/catapi/rest/')
    foto_dado = response.json()
    foto_gato = foto_dado['url']

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, disable_web_page_preview=True,
        parse_mode=telegram.ParseMode.HTML)

    context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=foto_gato, parse_mode=telegram.ParseMode.HTML)


def foto_cachorros(update, context):
    message = f'Olá, {update.message.from_user.first_name}! 😎\n'
    message += 'Olha o cachorrinho:'

    response = requests.get('https://dog.ceo/api/breeds/image/random')
    foto_dado = response.json()
    foto_gato = foto_dado['message']

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, disable_web_page_preview=True,
        parse_mode=telegram.ParseMode.HTML)

    context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=foto_gato, parse_mode=telegram.ParseMode.HTML)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("gatos", foto_gatos))
    dispatcher.add_handler(CommandHandler("cachorros", foto_cachorros))

    if DEBUG:
        updater.start_polling()

        updater.idle()
    else:
        port = config('PORT', cast=int)

        updater.start_webhook(listen="0.0.0.0",
                              port=port,
                              url_path=TELEGRAM_TOKEN)
        updater.bot.setWebhook(f'https://{APP_NAME_HEROKU}.herokuapp.com/{TELEGRAM_TOKEN}')

        updater.idle()


if __name__ == "__main__":
    print("Bot em execução.")
    main()
