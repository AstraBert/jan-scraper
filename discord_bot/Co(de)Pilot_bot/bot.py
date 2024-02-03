from discord import Client, File, Intents
from jan_scraper.scraper import scrape_jan_through_api
from jan_scraper.formatter import convert_code_to_curl_json
import os
import time
import pandas as pd

CHANNEL_ID = 0
TOKEN = ""



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
        model="deepseek-coder-1.3b",
        text=msg,
        name="Co(de)Pilot",
        new_instructions="You are an helpful python coding assistant",
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
        model="deepseek-coder-1.3b",
        text=msg,
        name="CodeCopilot",
        new_instructions="You are an helpful python coding assistant",
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
    leftovers = [str(i) for i in list(pd.read_csv("queue.csv")["JOB_ID"])]
    if len(leftovers) > 0:
        print("Cleaning job queue...")
        c = open("queue.csv", "r+")
        lines = c.readlines()
        c.seek(0)
        c.truncate()
        for line in lines:
            if line.split(",")[0] not in leftovers:
                c.write(line)
            else:
                continue
        c.close()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Print a confirmation
        print(f"Connected to the channel: {channel.name} ({channel.id})")

        # Send the welcome message
        await channel.send(f"The bot was activated at: {time.time()}")
    else:
        print(
            "Unable to find the specified channel ID. Make sure the ID is correct and the bot has the necessary permissions."
        )


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if message.attachments:
        print("Received files...")
        csv = pd.read_csv("queue.csv")
        queue = list(csv["JOB_ID"])
        print(
            f"Got content {message.content} from {message.author} ({type(message.author)})"
        )
        for attachment in message.attachments:
            await attachment.save("downloads/downloaded_file.py")
            if len(queue) == 0:
                job_time = time.time()
                job_author = message.author
                c = open("queue.csv", "a")
                c.write(f"{job_time},{str(job_author)}\n")
                c.close()
                print(f"Received file: {attachment.filename}")
                refactored_code = refactor_code(
                    "downloads/downloaded_file.py", str(attachment.filename)
                )
                with open(refactored_code, "rb") as file:
                    await message.channel.send(file=File(file))
                c = open("queue.csv", "r+")
                lines = c.readlines()
                c.seek(0)
                c.truncate()
                for line in lines:
                    if line.split(",")[0] != str(job_time) and line.split(",")[
                        1
                    ].replace("\n", "") != str(job_author):
                        c.write(line)
                    else:
                        continue
                c.close()
            else:
                await message.channel.send(
                    f"Hi {str(message.author)}! Your job was queued, please be patient..."
                )
                L = len(queue)
                while L > 0:
                    time.sleep(1)
                    csv = pd.read_csv("queue.csv")
                    queue = list(csv["JOB_ID"])
                    L = len(queue)
                    if L == 0:
                        break
                job_time = time.time()
                job_author = message.author
                c = open("queue.csv", "a")
                c.write(f"{job_time},{str(job_author)}\n")
                c.close()
                refactored_code = refactor_code(
                    "downloads/downloaded_file.py", str({attachment.filename})
                )
                with open(refactored_code, "rb") as file:
                    await message.channel.send(file=File(file))
                file.close()
                c = open("queue.csv", "r+")
                lines = c.readlines()
                c.seek(0)
                c.truncate()
                for line in lines:
                    if line.split(",")[0] != str(job_time) and line.split(",")[
                        1
                    ].replace("\n", "") != str(job_author):
                        c.write(line)
                    else:
                        continue
                c.close()
    elif message.content:
        csv = pd.read_csv("queue.csv")
        queue = list(csv["JOB_ID"])
        print(
            f"Got content {message.content} from {message.author} ({type(message.author)})"
        )
        if len(queue) == 0:
            job_time = time.time()
            job_author = message.author
            c = open("queue.csv", "a")
            c.write(f"{job_time},{str(job_author)}\n")
            c.close()
            newfile, generated_code = generate_code(message.content)
            await message.channel.send(generated_code)
            with open(newfile, "rb") as file:
                await message.channel.send(file=File(file))
        else:
            await message.channel.send(
                f"Hi {str(message.author)}! Your job was queued, please be patient..."
            )
            L = len(queue)
            while L > 0:
                time.sleep(1)
                csv = pd.read_csv("queue.csv")
                queue = list(csv["JOB_ID"])
                L = len(queue)
                if L == 0:
                    break
            job_time = time.time()
            job_author = message.author
            c = open("queue.csv", "a")
            c.write(f"{job_time},{str(job_author)}\n")
            c.close()
            newfile, generated_code = generate_code(message.content)
            await message.channel.send(generated_code)
            with open(newfile, "rb") as file:
                await message.channel.send(file=File(file))
            file.close()
            c = open("queue.csv", "r+")
            lines = c.readlines()
            c.seek(0)
            c.truncate()
            for line in lines:
                if line.split(",")[0] != str(job_time) and line.split(",")[1].replace(
                    "\n", ""
                ) != str(job_author):
                    c.write(line)
                else:
                    continue
            c.close()


bot.run(TOKEN)
