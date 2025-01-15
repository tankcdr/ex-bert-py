import os
import telebot

from dotenv import load_dotenv
from dl_translate import TranslationModel

######################################################################
# Telegram Translation Bot
######################################################################


######################################################################
# Configuration and setup
######################################################################

# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the .env file
env_path = os.path.join(script_dir, '../.env')
# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Get the Telegram bot API key and initialize the bot
bot_api_key = os.getenv("TELEGRAM_BOT_KEY")
bot = telebot.TeleBot(bot_api_key, parse_mode=None)

# Create the intent classifier
# intent_classifier = pipeline("zero-shot-classification")


def main():
    transalation_model = TranslationModel()

    print(transalation_model.available_languages())

    print(f"Translation: {transalation_model.translate(
        text="Hello", source="en", target="es")}")


if __name__ == "__main__":
    main()
