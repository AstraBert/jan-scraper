from discord import Client, File, Intents
from jan_scraper.scraper import scrape_jan_through_api
import os
import sqlite3
import time

CHANNEL_ID = 0
TOKEN = ""


def convert_code_to_curl_json(code):
    """
    Convert a Python code string to a format suitable for inclusion in a JSON string within a curl command.

    Parameters:
    - code (str): Python code string.

    Returns:
    - str: JSON-formatted string suitable for inclusion in a curl command.
    """
    # Escape backslashes and double quotes in the code
    escaped_code = code.replace('"', '\\\\\\"')

    # Replace newline characters with '\\n'
    formatted_code = escaped_code.replace("\n", "\\\\n")
    return formatted_code


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


def refactor_code(pydocument, filename):
    """Refactor Python code using jan_scraper."""
    f = open(pydocument, "r")
    lines = f.readlines()
    txt = "".join(lines)
    fmtcode = convert_code_to_curl_json(txt)
    msg = f"Refactor the following code\\n {fmtcode}"
    f.close()
    response = scrape_jan_through_api(
        app="/Users/Daniele/AppData/Local/Programs/jan/Jan.exe",
        model="deepseek-coder-1.3b",
        text=msg,
        name="Co(de)Pilot",
        new_instructions="You are an helpful python coding assistant",
        auto=False,
    )
    n = open("code.md", "w")
    n.write(response)
    n.close()
    m = open("code.md", "r")
    lines = m.readlines()
    m.close()
    blocks = get_python_code(lines)
    newname = os.path.join(
        "sent", os.path.basename(filename).split(".")[0] + "_refactored.py"
    )
    nnm = open(newname, "w")
    for i in blocks:
        nnm.write("".join(i) + "\n")
    nnm.close()
    return newname


def generate_code(message):
    """Generate Python code using jan_scraper."""
    msg = f"Write a python code to do the following\\n {message}"
    response = scrape_jan_through_api(
        app="/Users/Daniele/AppData/Local/Programs/jan/Jan.exe",
        model="deepseek-coder-1.3b",
        text=msg,
        name="CodeCopilot",
        new_instructions="You are an helpful python coding assistant",
        auto=False,
    )
    n = open("code.md", "w")
    n.write(response)
    n.close()
    m = open("code.md", "r")
    lines = m.readlines()
    m.close()
    fullmsg = "".join(lines)
    blocks = get_python_code(lines)
    print(blocks)
    newname = os.path.join("sent", "deepseek-coder_response.py")
    nnm = open(newname, "w")
    for i in blocks:
        nnm.write("".join(i) + "\n")
    nnm.close()
    return newname, fullmsg


intents = Intents.default()
intents.messages = True


bot = Client(intents=intents)


@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Print a confirmation
        print(f"Connected to the channel: {channel.name} ({channel.id})")

        # Send the welcome message
        await channel.send(
            f"The bot was activated at: {time.time()}"
        )
    else:
        print(
            "Unable to find the specified channel ID. Make sure the ID is correct and the bot has the necessary permissions."
        )


@bot.event
async def on_message(message):
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    
    if message.author == bot.user:
        return

    if message.attachments:
        print("Received files...")
        for attachment in message.attachments:
            await attachment.save("downloads/downloaded_file.py")
            post = connection.execute("SELECT * FROM queue").fetchall()
            if len(post) == 0:
                job_time = time.time()
                connection.execute(
                    "INSERT INTO queue (author, job_id) VALUES (?, ?)",
                    (str(message.author), job_time),
                )
                print(f"Received file: {attachment.filename}")
                refactored_code = refactor_code(
                    "downloads/downloaded_file.py", str(attachment.filename)
                )
                connection.execute("DELETE from queue WHERE job_id=?", (job_time,))
                with open(refactored_code, "rb") as file:
                    await message.channel.send(file=File(file))
            else:
                L = len(post)
                while L > 0:
                    L = len(post)
                    print("Job was queued")
                    time.sleep(2)
                job_time = time.time()
                connection.execute(
                    "INSERT INTO queue (author, job_id) VALUES (?, ?)",
                    (str(message.author), job_time),
                )
                refactored_code = refactor_code(
                    "downloads/downloaded_file.py", str({attachment.filename})
                )
                connection.execute("DELETE from queue WHERE job_id=?", (job_time,))
                with open(refactored_code, "rb") as file:
                    await message.channel.send(file=File(file))
    elif message.content:
        print(
            f"Got content {message.content} from {message.author} ({type(message.author)})"
        )
        post = connection.execute("SELECT * FROM queue").fetchall()
        if len(post) == 0:
            job_time = time.time()
            connection.execute(
                "INSERT INTO queue (author, job_id) VALUES (?, ?)",
                (str(message.author), job_time),
            )
            newfile, generated_code = generate_code(message.content)
            connection.execute("DELETE from queue WHERE job_id=?", (job_time,))
            await message.channel.send(generated_code)
            with open(newfile, "rb") as file:
                await message.channel.send(file=File(file))
        else:
            L = len(post)
            while L > 0:
                L = len(post)
                time.sleep(2)
            job_time = time.time()
            connection.execute(
                "INSERT INTO queue (author, job_id) VALUES (?, ?)",
                (str(message.author), job_time),
            )
            newfile, generated_code = generate_code(message.content)
            connection.execute("DELETE from queue WHERE job_id=?", (job_time,))
            await message.channel.send(generated_code)
            with open(newfile, "rb") as file:
                await message.channel.send(file=File(file))


bot.run(TOKEN)
