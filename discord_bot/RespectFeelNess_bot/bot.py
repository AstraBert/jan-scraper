from discord import Client, Intents
from jan_scraper.scraper import scrape_jan_through_api
import time
import pandas as pd


CHANNEL_ID = 1200892425946796195
TOKEN = "MTIwMTI2NTYwNTAwNTgwMzYzMg.G6e90S.qBXGr43CycqUSxM44SiAMPhjPlJ8uc8uCBMJ20"

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
    if message.author == bot.user:
        return
    
    elif message.content:
        csv = pd.read_csv("queue.csv")
        queue = list(csv["JOB_ID"])
        print(
            f"Got content {message.content} from {message.author} ({type(message.author)})"
        )
        if len(queue) == 0:
            job_time = time.time()
            job_author = message.author
            c = open("queue.csv","a")
            c.write(f"{job_time},{str(job_author)}\n")
            c.close()
            response = scrape_jan_through_api(str(message.content), app="/Users/Daniele/AppData/Local/Programs/jan/Jan.exe",model="llama2-chat-7b-q4",new_instructions="You are a wellbeing assistant focused on giving your best advice and psychological and emotional support to make people feel respected and accepted for who they are")
            c = open("queue.csv","r+")
            lines = c.readlines()
            c.seek(0)
            c.truncate()
            for line in lines:
                if line.split(",")[0] != str(job_time):
                    c.write(line)
                else:
                    continue
            c.close()
            await message.channel.send(response)
        else:
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
            c = open("queue.csv","a")
            c.write(f"{job_time},{str(job_author)}\n")
            c.close()
            response = scrape_jan_through_api(str(message.content), app="/Users/Daniele/AppData/Local/Programs/jan/Jan.exe",model="llama2-chat-7b-q4",new_instructions="You are a wellbeing assistant focused on making people feeling comfortable and respected at every moment")
            c = open("queue.csv","r+")
            lines = c.readlines()
            c.seek(0)
            c.truncate()
            for line in lines:
                if line.split(",")[0] != str(job_time):
                    c.write(line)
                else:
                    continue
            c.close()
            await message.channel.send(response)
        

    

bot.run(TOKEN)
