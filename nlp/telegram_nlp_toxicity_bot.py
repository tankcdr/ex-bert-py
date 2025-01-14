import os
import telebot

from dotenv import load_dotenv
from transformers import pipeline


# Load environment variables from .env file
# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the .env file
env_path = os.path.join(script_dir, '../.env')
load_dotenv(dotenv_path=env_path)

# bot_api_key = os.getenv("TELEGRAM_BOT_KEY")
# bot = telebot.TeleBot(bot_api_key, parse_mode=None)

# get our BART model
nlp_classifier = pipeline("zero-shot-classification")

customer_message = "I'd like to order a pizza"
customer_intents = ["choose drink", "order pizza", "inform my address"]

print(nlp_classifier(customer_message, customer_intents))
