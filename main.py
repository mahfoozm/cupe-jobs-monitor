import os 
from dotenv import load_dotenv
import discord
import requests
from bs4 import BeautifulSoup
import asyncio

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Connected")
    channel_id = discord.utils.get(client.get_all_channels(), name='general')
    await channel_id.send(f"Initialized")
    client.loop.create_task(check_website())

semesters = {0: "CUPE 1: 2022 S", 1: "CUPE 1: 2022 FW", 2: "CUPE 1: 2023 S",
             3: "CUPE 1: 2023 FW", 4: "CUPE 2: 2022 S", 5: "CUPE 2: 2022 FW",
             6: "CUPE 2: 2023 S", 7: "CUPE 2: 2023 FW", 8: "CUPE 3: 2022 S",
             9: "CUPE 3: 2022 FW", 10: "CUPE 3: 2023 S", 11: "CUPE 3: 2023 FW"}


async def check_website():
    prev_badge_data = []
    while True:
        website = requests.get("https://cupejobs.uit.yorku.ca/")
        soup = BeautifulSoup(website.content, "html.parser")
        div = soup.find("div", id="squelch-taas-tab-content-LE-post")
        badges = div.find_all("span", class_="badge")

        curr_badge_data = []
        for badge in badges:
            badge_text = badge.text
            curr_badge_data.append(badge_text)

        if not prev_badge_data:
            print("prev badge data initialized")
            prev_badge_data = curr_badge_data
            channel_id = discord.utils.get(client.get_all_channels(), name='general')
            await channel_id.send(f"Initialized with data: {prev_badge_data}")

        else:
            if prev_badge_data != curr_badge_data:
                for i in range(len(curr_badge_data)):
                    if prev_badge_data[i] != curr_badge_data[i]:
                        print(f"Detected a change in {semesters[i]}")
                        channel_id = discord.utils.get(client.get_all_channels(), name='general')
                        await channel_id.send(f"Job listings for {semesters[i]} has changed from {prev_badge_data[i]} to {curr_badge_data[i]}")
                prev_badge_data = curr_badge_data


        print (f"Previous badge data: {prev_badge_data}")
        print (f"Badge data: {curr_badge_data}")
        await asyncio.sleep(21600) # 6 hours

load_dotenv()
client.run(os.getenv("TOKEN"))
