"""This user case walks you through building a python copilot exploiting deepseek-coder-1.3b 
in Jan (you have to download it if you want this project to function). 
The result will be a Telegram bot that will respond to your code inquiries and will refactor your python code."""


from jan_scraper.scraper import scrape_jan_through_api
from jan_scraper.formatter import convert_code_to_curl_json
from telegram.ext import *
import os
import emoji

SPECIAL_CHARS = [
  '\\',
  '_',
  '*',
  '[',
  ']',
  '(',
  ')',
  '~',
  '`',
  '>',
  '<',
  '&',
  '#',
  '+',
  '-',
  '=',
  '|',
  '{',
  '}',
  '.',
  '!'
]

async def start_commmand(update, context):
    """Handle the /start command."""
    await update.message.reply_text(emoji.emojize(f"Hi, this is your Python:snake: Copilot Bot: I am here to help you in everything you need with python! If you want me to refactor your code, just send me your python file and I'll do it. If you have an idea and don't know how to deal with it, write me a quick message! :winking_face_with_tongue:"))

async def help_command(update, context):
    """Handle the /help command."""
    await update.message.reply_text(emoji.emojize(f"Examples of messages you can send:\n\n:linked_paperclips::page_facing_up:bot.py\n(this is to refactor the code in bot.py)\n\nEhi, can you tell me how to print a string in python?"))


def get_python_code(lines):
    """Extract Python code blocks from a list of lines."""
    blocks = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith("```python"):
            i += 1
        else:
            j = i + 1
            blocks.append([])
            while not lines[j].startswith("```") or j == len(lines) - 1:
                if lines[j].startswith("```") or j == len(lines) - 1:
                    break
                else:
                    blocks[len(blocks) - 1].append(lines[j])
                    j += 1
            if j < len(lines) - 1:
                i = j + 1
            else:
                break
    for i in range(len(blocks)):
        for j in range(len(blocks[i])):
            if j < len(blocks[i]):
                if blocks[i][j].startswith("```"):
                    blocks[i].remove(blocks[i][j])
                else:
                    pass
    return blocks

def refactor_code(pydocument):
    """Refactor Python code using jan_scraper."""
    f = open(pydocument, "r")
    lines = f.readlines()
    txt = "".join(lines)
    fmtcode = convert_code_to_curl_json(txt)
    msg = f"Refactor the following code\\n {fmtcode}"
    f.close()
    response = scrape_jan_through_api(app="jan/Jan.exe", model="deepseek-coder-1.3b", text=msg, name="CodeCopilot", new_instructions="You are an helpful coding assistant", auto=False)
    n = open("code.md", "w")
    n.write(response)
    n.close()
    m = open("code.md", "r")
    lines = m.readlines()
    m.close()
    blocks = get_python_code(lines)
    newname = os.path.join("code", os.path.basename(pydocument).split(".")[0] + "_refactored.py")
    nnm = open(newname, "w")
    for i in blocks:
        nnm.write("".join(i) + "\n")
    nnm.close()
    return newname

def generate_code(message):
    """Generate Python code using jan_scraper."""
    msg = f"Write a python code to do the following\\n {message}"
    response = scrape_jan_through_api(app="jan/Jan.exe", model="deepseek-coder-1.3b", text=msg, name="CodeCopilot", new_instructions="You are an helpful coding assistant", auto=False)
    n = open("code.md", "w")
    n.write(response)
    n.close()
    m = open("code.md", "r")
    lines = m.readlines()
    m.close()
    fullmsg = "".join(lines)
    blocks = get_python_code(lines)
    print(blocks)
    newname = os.path.join("code", "deepseek-coder_response.py")
    nnm = open(newname, "w")
    for i in blocks:
        nnm.write("".join(i) + "\n")
    nnm.close()
    return newname, fullmsg

async def refactor_code_from_file(update, context) -> None:
    """Handle refactoring Python code from a file."""
    user = update.message.from_user
    print(user)
    if update.message.document:
        doc = update.message.document
        inf = "downloaded_from_user.py"
        fid = doc.file_id
        print(fid)
        # Download the file from Telegram to the local directory
        await (await context.bot.get_file(fid)).download(inf)
        # Refactor the code
        refactored_code = refactor_code(inf)
        await update.message.reply_document(document=open(refactored_code, 'rb'))

async def generate_code_from_prompt(update, context):
    """Handle generating Python code from a prompt."""
    prompt = update.message.text
    file_to_reply, fullanswer = generate_code(prompt)
    for i in SPECIAL_CHARS:
        fullanswer = fullanswer.replace(i, "\\" + i)
    await update.message.reply_text(fullanswer, parse_mode="MarkdownV2")
    await update.message.reply_document(document=open(file_to_reply, 'rb'))

async def error_handler(update, context: CallbackContext) -> None:
    """Log the error and send a message to the user."""
    print(f"An error occurred: {context.error}")
    await update.message.reply_text("Sorry, something went wrong.")

TOKEN = ""

if __name__ == '__main__':
    print("Bot is high and running")
    application = Application.builder().token(TOKEN).build()
    # Commands
    application.add_handler(CommandHandler('start', start_commmand))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.Document.PY, refactor_code_from_file))
    application.add_handler(MessageHandler(filters.TEXT, generate_code_from_prompt))
    application.add_error_handler(error_handler)
    # Run bot
    application.run_polling(1.0)

