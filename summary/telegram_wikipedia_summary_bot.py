import os
import telebot

from dotenv import load_dotenv
from transformers import pipeline


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

bot_api_key = os.getenv("TELEGRAM_BOT_KEY")

bot = telebot.TeleBot(bot_api_key, parse_mode=None)

summarization_text = "The Who are an English rock band formed in London in 1964. Their classic lineup consisted of lead singer Roger Daltrey, guitarist and singer Pete Townshend, bass guitarist and singer John Entwistle, and drummer Keith Moon. They are considered one of the most influential rock bands of the 20th century and have sold over 100 million records worldwide. Their contributions to rock music include the development of the Marshall stack, large PA systems, the use of the synthesizer, Entwistle and Moon''s influential playing styles, Townshend''s feedback and power chord guitar technique, and the development of the rock opera. They are cited as an influence by many hard rock, punk rock, and mod bands, and their songs still receive regular exposure."


def main():
    summarizer = pipeline("summarization")

    print(summarizer(summarization_text, max_length=20,
          min_length=5, do_sample=False))

    sumt5 = pipeline("summarization", model="t5-base", tokenizer="t5-base")
    print(sumt5(summarization_text, max_length=20,
          min_length=5, do_sample=False))

    title_gen = pipeline(
        "summarization", model="moussaKam/barthez-orangesum-title")
    print(title_gen(summarization_text))


if __name__ == "__main__":
    main()
