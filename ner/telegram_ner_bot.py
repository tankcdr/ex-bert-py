import os
import telebot

from dotenv import load_dotenv
from transformers import pipeline
from dl_translate import TranslationModel

######################################################################
# Telegram Named Entity Bot
######################################################################


######################################################################
# Configuration and setup
######################################################################

# # Get the absolute path of the directory where the script is located
# script_dir = os.path.dirname(os.path.abspath(__file__))
# # Construct the full path to the .env file
# env_path = os.path.join(script_dir, '../.env')
# # Load environment variables from .env file
# load_dotenv(dotenv_path=env_path)
#
# # Get the Telegram bot API key and initialize the bot
# bot_api_key = os.getenv("TELEGRAM_BOT_KEY")
# bot = telebot.TeleBot(bot_api_key, parse_mode=None)


######################################################################
# Implementation
######################################################################

def main():
    ner = pipeline("ner", aggregation_strategy="simple")
    print(ner("My name is Rocky Balboa and I live in Philly. I train at Mighty Mick's Gym."))


if __name__ == "__main__":
    main()
