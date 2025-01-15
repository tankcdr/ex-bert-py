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
    ner = pipeline("ner", model="blaze999/Medical-NER",
                   tokenizer="blaze999/Medical-NER", aggregation_strategy="simple")

    print(ner("Take 1mg of Tylenol every 12 hours for 5 days."))


if __name__ == "__main__":
    main()
