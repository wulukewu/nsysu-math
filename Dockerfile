# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies and chromedriver
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
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

# Run the main.py script
CMD ["python", "main.py"]