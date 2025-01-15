import os
import telebot
import wikipedia

from dotenv import load_dotenv
from transformers import pipeline


######################################################################
# Telegram Bot supporting Wikipedia Summarization
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

summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")

# state
user_states = {}

#################################################################
# Wikipedia Summarization Bot Implementation
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

        # this doesn't always work for the best
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
            message, "Hello! Please enter a topic you would like a brief summary about.")

    elif state == 1:
        # State 1: User has entered a topic and we need to fetch the context
        user_states[message.from_user.id] = 0
        context = get_wikipedia_content_for_topic(message.json["text"])

        if context is None:
            bot.reply_to(
                message, "Sorry, I couldn't find any relevant information on Wikipedia.")
            user_states[message.from_user.id] = 0
            return

        summary = summarizer(context, max_length=100,
                             min_length=5, do_sample=False)

        bot.reply_to(message, summary[0]["summary_text"])

    else:
        bot.reply_to(
            message, "Sorry, I've had an internal error. Please start again.")


bot.infinity_polling()
