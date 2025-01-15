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

# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the .env file
env_path = os.path.join(script_dir, '../.env')
# Load environment variables from .env file
load_dotenv(dotenv_path=env_path)

# Get the Telegram bot API key and initialize the bot
bot_api_key = os.getenv("TELEGRAM_BOT_KEY")
bot = telebot.TeleBot(bot_api_key, parse_mode=None)

# setup the pipeline
ner = pipeline("ner", model="samrawal/bert-large-uncased_med-ner",
               tokenizer="samrawal/bert-large-uncased_med-ner", aggregation_strategy="simple")


######################################################################
# Implementation
######################################################################
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    """Handles the incoming messages from the user.
       Simple named entity recognition using the transformers pipeline.
    """
    entities = ner(message.text)

    medication = "not found"
    dosage = "not found"
    frequency = "not found"
    duration = "not found"

    for entity in entities:
        if entity["entity_group"] == "do":
            dosage = entity["word"]
        elif entity["entity_group"] == "m":
            medication = entity["word"]
        elif entity["entity_group"] == "f":
            frequency = entity["word"]
        elif entity["entity_group"] == "du":
            duration = entity["word"]

    bot.reply_to(
        message, f"Medication: {medication} --Dosage: {dosage} --Frequency: {frequency} --Duration: {duration}.")


bot.infinity_polling()
