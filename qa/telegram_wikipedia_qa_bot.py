import os
import telebot
import wikipedia
import nltk
import re

from dotenv import load_dotenv
from transformers import pipeline
from rank_bm25 import BM25Okapi
from nltk.tokenize import sent_tokenize, word_tokenize

# Load environment variables from .env file
load_dotenv()
bot_api_key = os.getenv("TELEGRAM_BOT_KEY")

bot = telebot.TeleBot(bot_api_key, parse_mode=None)

nltk.download("punkt_tab")
basic_classifier = pipeline("question-answering",
                            model="deepset/roberta-base-squad2",
                            tokenizer="deepset/roberta-base-squad2")

# state
user_states = {}
user_context = {}

#################################################################
# Wikipedia Question Answering Bot
#################################################################


def get_wikipedia_content_for_topic(topic):
    """Get the wikipedia content for the specified topic.

    Args:
        topic (string): The topic to search for on Wikipedia.

    Returns:
        string: The summary of the Wikipedia page for the topic.
        None: If no relevant Wikipedia page is found.
    """
    try:
        search_results = wikipedia.search(topic)

        if not search_results:
            print("No relevant Wikipedia page found.")
            return None

        page = wikipedia.summary(search_results[0])
        return page

    except wikipedia.DisambiguationError as e:
        # Handle disambiguation by selecting the first option
        page = wikipedia.summary(e.options[0])
        return page

    except wikipedia.PageError:
        print("Wikipedia page does not exist.")
        return None


# Telegram bot handler
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    """Simple Telegram handler that manages user state and replies to messages.
    """
    state = user_states.get(message.from_user.id, None)

    if state == 0 or state is None:
        # State 0: User has not started a conversation.
        # If the user hasn't been here before, then state will be None
        user_states[message.from_user.id] = 1
        bot.reply_to(
            message, "Hello! Please enter a topic you would like to talk about.")

    elif state == 1:
        # State 1: User has entered a topic and we need to fetch the context
        user_states[message.from_user.id] = 2
        context = get_wikipedia_content_for_topic(message.json["text"])

        if context is None:
            bot.reply_to(
                message, "Sorry, I couldn't find any relevant information on Wikipedia.")
            user_states[message.from_user.id] = 0
            return

        user_context[message.from_user.id] = context
        bot.reply_to(message, "Please ask a question.")

    elif state == 2:
        # State 2: User has entered a question and we need to answer it

        if message.json["text"].lower() == "end":
            # if user wants to end the conversation
            user_states[message.from_user.id] = 0
            user_states.pop(message.from_user.id, None)
            bot.reply_to(message, "Goodbye!")
            return

        context = user_context.get(message.from_user.id, None)

        if context is None:
            bot.reply_to(
                message, "Sorry, I lost the context. Please start again.")
            user_states[message.from_user.id] = 0
            return

        question = message.json["text"]
        answer = basic_classifier(question=question, context=context)

        if answer is None:
            bot.reply_to(
                message, "Sorry, I couldn't find an answer to your question. Please try again or enter 'end' to exit.")
            return

        bot.reply_to(
            message, answer["answer"] + "\n\nPlease ask another question or enter 'end' to exit.")

    else:
        bot.reply_to(
            message, "Sorry, I've had an internal error. Please start again.")


bot.infinity_polling()
