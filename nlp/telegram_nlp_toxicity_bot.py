import os
import telebot

from dotenv import load_dotenv
from transformers import pipeline, TextClassificationPipeline, AutoTokenizer, AutoModelForSequenceClassification

######################################################################
# Telegram Bot for Natural Language Processing and Toxicity Detection
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
intent_classifier = pipeline("zero-shot-classification")
handled_intents = ["choose drink", "order pizza",
                   "inform my address", "something else"]

# Create the toxicity classifier
toxicity_model = 'unitary/toxic-bert'  # could make this a env variable
toxicity_tokenizer = AutoTokenizer.from_pretrained(toxicity_model)
toxcity_model = AutoModelForSequenceClassification.from_pretrained(
    toxicity_model)

toxicity_classifier = TextClassificationPipeline(
    # pt = PyTorch, that is what we are using
    model=toxcity_model, tokenizer=toxicity_tokenizer, framework="pt")


######################################################################
# Implementation
######################################################################
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    """Handles the incoming messages from the user.
       First checks the toxicity of the message and then processes it.
            Toxic messages are not processed.
       Then classifies the intent of the message and responds accordingly.

    Args:
        message (string): Inbound message structure from the user.
    """
    # first check the toxcity of the message
    toxicity = toxicity_classifier(message.text)

    if toxicity[0]['score'] > 0.8:
        bot.reply_to(message, "I'm sorry, I cannot respond to toxic messages.")
        return

    # classify the intent of the message
    intent_classifier_output = intent_classifier(message.text, handled_intents)
    print(intent_classifier_output)
    labels = intent_classifier_output["labels"]
    scores = intent_classifier_output["scores"]
    detected_intents = [label for label,
                        score in zip(labels, scores) if score > 0.55]

    print(detected_intents)

    if not detected_intents:
        bot.reply_to(
            message, "I am simple bot that detects toxcity and if you want to order a pizza.")
        return

    # handle the detected intents
    for intent in detected_intents:
        if intent == "choose drink":
            bot.reply_to(message, "Detected intent: choose drink")
        elif intent == "order pizza":
            bot.reply_to(message, "Detected intent: order pizza")
        elif intent == "inform my address":
            bot.reply_to(message, "Detected intent: inform my address")
        else:
            bot.reply_to(
                message, "I am simple bot that detects toxcity and if you want to order a pizza.")


bot.infinity_polling()
