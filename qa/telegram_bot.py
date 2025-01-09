import os
import telebot

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

bot_api_key = os.getenv("TELEGRAM_BOT_KEY")

bot = telebot.TeleBot(bot_api_key, parse_mode=None)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "hello")


bot.infinity_polling()
