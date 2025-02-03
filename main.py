import os
from dotenv import load_dotenv

import time
from datetime import datetime, timedelta, timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import discord

def get_taiwan_date():
    # Get the current UTC time
    now_utc = datetime.now(timezone.utc)

    # Convert to UTC+8
    now_utc_plus_8 = now_utc + timedelta(hours=8)

    # Calculate Taiwan year
    taiwan_year = now_utc_plus_8.year - 1911

    # Format the time as 'YYY.MM.DD'
    formatted_time = f"{taiwan_year:03}.{now_utc_plus_8.month:02}.{now_utc_plus_8.day:02}"

    return formatted_time

def dc_send(message, token, guild_id, channel_id):

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        guild = discord.utils.get(client.guilds, id=guild_id)
        channel = discord.utils.get(guild.channels, id=channel_id)
        await channel.send(message)
        await client.close()

    client.run(token)

# Load environment variables from .env file
load_dotenv()

# Get environment variables with error handling
discord_token = os.getenv('DISCORD_TOKEN')
if not discord_token:
    raise ValueError("DISCORD_TOKEN environment variable not set")

discord_guild_id = os.getenv('DISCORD_GUILD_ID')
if not discord_guild_id:
    raise ValueError("DISCORD_GUILD_ID environment variable not set")
discord_guild_id = int(discord_guild_id)

discord_channel_id = os.getenv('DISCORD_CHANNEL_ID')
if not discord_channel_id:
    raise ValueError("DISCORD_CHANNEL_ID environment variable not set")
discord_channel_id = int(discord_channel_id)

def format_message(input_date, input_message):
    if '\n' not in input_message:
        return f'{input_date}: {input_message}'
    else:
        return f'{input_date}:\n{input_message}'

# Set up ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')

driver = webdriver.Chrome(options=options)

driver.get('https://www.math.nsysu.edu.tw/~problem/')

# time.sleep(3)

# Get the URL from the specified XPath
frame_element = driver.find_element(By.XPATH, '/html/frameset/frameset/frame[2]')
frame_url = frame_element.get_attribute('src')
print(f'URL of the frame: {frame_url}')

# # Get the page source and parse it with BeautifulSoup
# page_source = driver.page_source
# soup = BeautifulSoup(page_source, 'html.parser')

# # Print the prettified HTML
# print(soup.prettify())

driver.get(frame_url)

table_element = driver.find_element(By.XPATH, '/html/body/div/table')
rows = table_element.find_elements(By.TAG_NAME, 'tr')

now_date = get_taiwan_date()

# Iterate over the rows from the last to the first
for row in reversed(rows):
    columns = row.find_elements(By.TAG_NAME, 'td')
    if len(columns) >= 2:
        announced_date = columns[0].text.strip()
        announced_message = columns[1].text
        # print(f'announced_date: {announced_date}, announced_message: {announced_message}')

        if announced_date == now_date:
            print('[INFO] Sending message to the Discord channel...')
            
            message = format_message(announced_date, announced_message)
            print(message)
            dc_send(message, discord_token, discord_guild_id, discord_channel_id)

    else:
        print('No columns found')
        break

driver.quit()