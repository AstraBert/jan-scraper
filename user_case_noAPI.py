"""
This project walks you through building a simple, user-customizable, Telegram bot, that will exploit jan-scraper to respond
"""

from telegram.ext import *
import emoji
from jan_scraper.scraper import scrape_jan
import sys

TOKEN = "" # Go on BotFather, set up a bot and retrieve the API token, than place it here

jan_app = "/Users/User/AppData/Local/Programs/jan/Jan.exe" #Generally this is the path for Windows, replace with yours
jan_threads = "/Users/User/jan/threads" #Generally this is the path for Windows, replace with yours 
instructions = "You are an helpful assistant" 
assistant_name = "Jan"
llm_model = "tinyllama-1.1b" #Replace with your default LLM model
new_thread = True
available_models = ["gpt-4","gpt-3.5-turbo","tinyllama-1.1b"] #Replace with your available LLM models


async def start_commmand(update, context):
    """Initialize the bot giving useful information about what it can do"""
    await update.message.reply_text(emoji.emojize(f"Here is the list of commands you can use:\n\n-/start: initialize the bot:SOON_arrow:\n\n-/name: input a name for your assistant after the command:rose:\n\n-/models_list: see the list of available models\n\n-/model: choose your preferred model among the available ones by writing it after the command\n\n-/instructions: give special instructions to your assistant, reporting them after the command:bookmark_tabs:\n\n-/conversation: activate or deactivate conversation mode:speaking_head:\n\n-/help: show the help message:raised_hand:"))

async def help_command(update, context):
    """Example of what can be done with the bot"""
    await update.message.reply_text(emoji.emojize(f"Here is an example of the messages you can send:\n\n/name Guglielmo Scuotipera\n\n/models_list\n\n-/model tinyllama-1.1b\n\n-/instructions You are an italian XVII century poet, who imitates Shakespeare\n\n/conversation\n\n/help"))

async def display_available_models_command(update, context):
    """Display all the available LLM models"""
    avs = '\n\n-'.join(available_models)
    await update.message.reply_text(emoji.emojize(f"Here are all the models you can use:\n\n-{avs}"))

async def choose_model_command(update, context):
    """Choose one of the available models"""
    global llm_model
    text =  update.message.text
    t = text.replace("/model ","")
    llm_model = t
    await update.message.reply_text(emoji.emojize(f"All right, you'll be using {llm_model} from now on!:robot:"))

async def conversation_mode_command(update, context):
    """Activate or deactivate conversation mode: this would mean that Jan assistan won't state a new chat thread if conversation mode is active, whereas it will start a new one if it isn't"""
    global new_thread
    if new_thread:
        new_thread = False
        await update.message.reply_text(emoji.emojize(f"Conversation mode activated!:rocket:"))
    else:
        new_thread = True
        await update.message.reply_text(emoji.emojize(f"Conversation mode deactivated!:rocket:"))

async def instructions_command(update, context):
    """Update assistant instructions"""
    global instructions
    text =  update.message.text
    t = text.replace("/instructions ","")
    instructions = t
    await update.message.reply_text(emoji.emojize(f"Perfect, assistant is now set as: {instructions}:bookmark_tabs:"))

async def name_command(update, context):
    """Give a name to the assistant"""
    global assistant_name
    text =  update.message.text
    t = text.replace("/name ","")
    assistant_name = t
    await update.message.reply_text(emoji.emojize(f"Cool! Your assistant will be named {assistant_name}:partying_face:"))

async def chat_with_assistant(update, context):
    """Interact with the assistant by sending message and retrieving the response"""
    text = update.message.text
    response = scrape_jan(text=text,app=jan_app,jan_threads_path=jan_threads,model=llm_model,name=assistant_name,new_instructions=instructions,set_new_thread=new_thread)
    await update.message.reply_text(emoji.emojize(f"{response}"))


async def unrecognized_command(update,context):
    """Handle unrecognized commands"""
    text =  update.message.text
    if text.startswith("/start")==False or text.startswith("/help")==False or text.startswith("/model")==False or text.startswith("/conversation")==False or text.startswith("/instructions")==False or text.startswith("/name") or text.startswith("/models_list")==False:
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
        application.add_handler(MessageHandler(filters.TEXT, chat_with_assistant))
        application.add_error_handler(error_handler)
        # Run bot
        application.run_polling(1.0)
    except KeyboardInterrupt:
        sys.exit(0)
