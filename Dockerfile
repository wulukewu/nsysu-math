# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies and Chromium
RUN apt-get update && \
    apt-get install -y wget unzip chromium && \
    apt-get clean

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Accept build arguments for environment variables
ARG DISCORD_TOKEN
ARG DISCORD_GUILD_ID
ARG DISCORD_CHANNEL_ID

# Set environment variables
ENV DISCORD_TOKEN=${DISCORD_TOKEN}
ENV DISCORD_GUILD_ID=${DISCORD_GUILD_ID}
ENV DISCORD_CHANNEL_ID=${DISCORD_CHANNEL_ID}

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# Update webdriver manager to use the chrome version and automatically download compatible driver version
RUN pip install --upgrade webdriver-manager

# Run the main.py script
CMD ["python", "main.py"]