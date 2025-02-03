import os
from dotenv import load_dotenv

import time
from datetime import datetime, timedelta, timezone

from selenium import webdriver
from selenium.webdriver.common.by import By

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
    # Set up Discord client with default intents
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        # Print login information
        print(f'We have logged in as {client.user}')
        # Get the guild (server) by ID
        guild = discord.utils.get(client.guilds, id=guild_id)
        # Get the channel by ID
        channel = discord.utils.get(guild.channels, id=channel_id)
        # Send the message to the channel
        await channel.send(message)
        # Close the client after sending the message
        await client.close()

    # Run the Discord client with the provided token
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
    # Format the message with the date and message content
    if '\n' not in input_message:
        return f'{input_date}: {input_message}'
    else:
        return f'{input_date}:\n{input_message}'

# Set up ChromeDriver with options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')

# Initialize the ChromeDriver
driver = webdriver.Chrome(options=options)

# Navigate to the specified URL
driver.get('https://www.math.nsysu.edu.tw/~problem/')

# Get the URL from the specified XPath
frame_element = driver.find_element(By.XPATH, '/html/frameset/frameset/frame[2]')
frame_url = frame_element.get_attribute('src')
print(f'URL of the frame: {frame_url}')

# Navigate to the frame URL
driver.get(frame_url)

# Find the table element
table_element = driver.find_element(By.XPATH, '/html/body/div/table')
# Get all rows in the table
rows = table_element.find_elements(By.TAG_NAME, 'tr')

# Get the current date in Taiwan format
now_date = get_taiwan_date()

# Iterate over the rows from the last to the first
for row in reversed(rows):
    # Get all columns in the row
    columns = row.find_elements(By.TAG_NAME, 'td')
    if len(columns) >= 2:
        # Extract the date and message from the columns
        announced_date = columns[0].text.strip()
        announced_message = columns[1].text

        # Check if the announced date matches the current date
        if announced_date == now_date:
            print('[INFO] Sending message to the Discord channel...')
            
            # Format the message
            message = format_message(announced_date, announced_message)
            print(message)
            # Send the message to the Discord channel
            dc_send(message, discord_token, discord_guild_id, discord_channel_id)
    else:
        print('No columns found')
        break

# Quit the driver
driver.quit()