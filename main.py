import os
from dotenv import load_dotenv

import time
from datetime import datetime, timedelta, timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

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

def dc_send_file(file_path, token, guild_id, channel_id):
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
        # Send the file to the channel
        await channel.send(file=discord.File(file_path))
        # Close the client after sending the file
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

# Navigate to the home problem page
driver.get('https://www.math.nsysu.edu.tw/~problem/')

# Get the URL of news frame
news_frame_element = driver.find_element(By.XPATH, '/html/frameset/frameset/frame[2]')
news_frame_url = news_frame_element.get_attribute('src')
print(f'URL of the news frame: {news_frame_url}')

# Get the URL of title frame
title_frame_element = driver.find_element(By.XPATH, '/html/frameset/frameset/frame[1]')
title_frame_url = title_frame_element.get_attribute('src')
print(f'URL of the title frame: {title_frame_url}')

# Navigate to the news frame URL
driver.get(news_frame_url)

# Find the table element
table_element = driver.find_element(By.XPATH, '/html/body/div/table')
# Get all rows in the table
rows = table_element.find_elements(By.TAG_NAME, 'tr')

# Get the current date in Taiwan format
now_date = get_taiwan_date()

# Initialize the number of files to send
files_num_to_send = 0

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

            # Check if the message contains the announcement
            if "題目已於本日公佈" in announced_message:
                files_num_to_send = 2
            else:
                files_num_to_send = 1

            print('[INFO] Sending message to the Discord channel...')
            
            # Format the message
            message = format_message(announced_date, announced_message)
            print(message)
            # Send the message to the Discord channel
            dc_send(message, discord_token, discord_guild_id, discord_channel_id)
    else:
        print('No columns found')
        break

# Check if there are files to send
if files_num_to_send > 0:
    # Send the files to the Discord channel
    print(f'[INFO] Sending {files_num_to_send} file{"s" if files_num_to_send > 1 else ""} to the Discord channel...')

    # Create the directory if it doesn't exist
    os.makedirs('./files', exist_ok=True)

    # Navigate to the title frame URL
    driver.get(title_frame_url)

    # Get the URL of problem frame
    problem_frame_element = driver.find_element(By.XPATH, '/html/body/div/table/tbody/tr[3]/td/p/b/span/a')
    problem_frame_url = problem_frame_element.get_attribute('href')
    print(f'URL of the frame: {problem_frame_url}')

    # Navigate to the problem frame URL
    driver.get(problem_frame_url)

    frame_element = driver.find_element(By.XPATH, '/html/body/div')
    paragraphs = frame_element.find_elements(By.TAG_NAME, 'p')

    file_urls = []
    for paragraph in reversed(paragraphs):
        # print(paragraph.text)
        # Check if there is an <a> tag inside the paragraph
        a_tags = paragraph.find_elements(By.TAG_NAME, 'a')
        if a_tags:
            for a_tag in a_tags:
                url = a_tag.get_attribute('href')
                if url:
                    file_urls.append(url)
                    if len(file_urls) == files_num_to_send:
                        break
        if len(file_urls) == files_num_to_send:
            break
    # print(file_urls)

    for file_url in file_urls:
        # Download the file
        response = requests.get(file_url, verify=False)
        file_name = os.path.join('./files', os.path.basename(file_url))

        with open(file_name, 'wb') as file:
            file.write(response.content)
            print(f'Downloaded {file_name}')

        # Send the downloaded file to the Discord channel
        dc_send_file(file_name, discord_token, discord_guild_id, discord_channel_id)


# Quit the driver
driver.quit()