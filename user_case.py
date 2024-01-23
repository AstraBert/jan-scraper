"""
This project walks you through building a simple, user-customizable, Telegram bot, that will exploit jan-scraper to respond
"""

from telegram.ext import *
import emoji
from jan_scraper.scraper import scrape_jan
import sys

TOKEN = ""

jan_app = ""
jan_threads = ""
instructions = ""
assistant_name = ""
llm_model = ""
new_thread = True



async def start_commmand(update, context):
    await update.message.reply_text(emoji.emojize(f""))

async def help_command(update, context):
    await update.message.reply_text(emoji.emojize(f""))

async def display_available_models_command(update, context):
    await update.message.reply_text(emoji.emojize(f"Here are all the models you can use:\n\n-tinyllama-1.1b: For starters, the tiniest llama on Earth will be helping you for basic requests...:llama:"))

async def choose_model_command(update, context):
    global llm_model
    text =  update.message.text
    t = text.replace("/model","")
    llm_model = t
    await update.message.reply_text(emoji.emojize(f"All right, you'll be using {llm_model} from now on!:robot:"))

async def conversation_mode_command(update, context):
    global new_thread
    new_thread = False
    await update.message.reply_text(emoji.emojize(f"Coversation mode activated!:rocket:"))

async def instructions_command(update, context):
    global instructions
    text =  update.message.text
    t = text.replace("/model","")
    instructions = t
    await update.message.reply_text(emoji.emojize(f"Perfect, assistant is now set as: {instructions}"))

async def name_command(update, context):
    global assistant_name
    text =  update.message.text
    t = text.replace("/model","")
    assistant_name = t
    await update.message.reply_text(emoji.emojize(f"Cool! Your assistant will be named {assistant_name}:partying_face:"))

async def unrecognized_command(update,context):
    text =  update.message.text
    if text.startswith("/start")==False or text.startswith("/help")==False or text.startswith("/model")==False or text.startswith("/conversation")==False or text.startswith("/instructions")==False or text.startswith("/name") or text.startswith("models_list"):
        await update.message.reply_text(f"I cannot understand the message:\n\"{text}\"\nAs my programmer did not insert it among the command I am set to respond: please check for misspelling/errors or contact the programmer if you feel anything is wrong/missing")
    else:
        pass


async def error_handler(update, context: CallbackContext) -> None:
    """Log the error and send a message to the user."""
    print(f"An error occurred: {context.error}")
    await update.message.reply_text("Sorry, something went wrong.")

if __name__ == '__main__':
    try:
        print("Bot is high and running")
        application = Application.builder().token(TOKEN).build()
        # Commands
        application.add_handler(CommandHandler('start', start_commmand))
        application.add_handler(CommandHandler('help', help_command))
        application.add_handler(CommandHandler('name', name_command))
        application.add_handler(CommandHandler('conversation', conversation_mode_command))
        application.add_handler(CommandHandler('instructions', instructions_command))
        application.add_handler(CommandHandler('model', choose_model_command))
        application.add_handler(CommandHandler('models_list', display_available_models_command))
        application.add_handler(MessageHandler(filters.COMMAND, unrecognized_command))
        application.add_error_handler(error_handler)
        # Run bot
        application.run_polling(1.0)
    except KeyboardInterrupt:
        sys.exit(0)
