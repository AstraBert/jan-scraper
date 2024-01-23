"""
This project walks you through building a simple, user-customizable, Telegram bot, that will exploit jan-scraper to respond
"""

from telegram.ext import *
import emoji
from jan_scraper.scraper import scrape_jan

TOKEN = ""

async def start_commmand(update, context):
    await update.message.reply_text(emoji.emojize(f""))

async def help_command(update, context):
    await update.message.reply_text(emoji.emojize(f""))

async def unrecognized_command(update,context):
    text =  update.message.text
    if text.startswith("/start")==False or text.startswith("/help")==False:
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
        application.add_handler(MessageHandler(filters.COMMAND, unrecognized_command))
        application.add_error_handler(error_handler)
        # Run bot
        application.run_polling(1.0)
    except KeyboardInterrupt:
        sys.exit(0)
