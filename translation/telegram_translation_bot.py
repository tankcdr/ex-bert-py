import os
import telebot

from dotenv import load_dotenv
from transformers import pipeline
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

# Create our BART
detector = pipeline("zero-shot-classification")
src_languages = ["german", "english"]
tgt_languages = ["Arabic", "Chinese", "French", "Italian",
                 "Japanese", "Korean", "Portuguese", "Russian", "Spanish"]

# Create the translation model
translator = TranslationModel()

# state
user_state = {}

######################################################################
# Implementation
######################################################################


@bot.message_handler(func=lambda m: True)
def translate(message):
    """Handles incoming messages from the user

    """
    user_message = message.text
    user_id = message.from_user.id

    if user_message.capitalize() in tgt_languages:
        user_state[user_id] = {"target_language": user_message}
        bot.reply_to(message, f"""Target language set to {
                     user_message}. Please enter the text you would like to translate to {user_message}.""")
        return

    if not user_id in user_state:
        bot.reply_to(message, f"""Hi! I translate English or German to other languages. Please select a target language from the following options to continue: {
                     tgt_languages}""")
        return

    if user_id in user_state:
        target_language = user_state[user_id]["target_language"]
        detected_language = detector(user_message, src_languages)

        translated_text = translator.translate(
            text=user_message, source=detected_language['labels'][0], target=target_language)

        bot.reply_to(message, f"""Translation to {
                     target_language}: {translated_text}.\nContinue translating or select a new target language.""")
        return


bot.infinity_polling()


if __name__ == "__main__":
    pass
