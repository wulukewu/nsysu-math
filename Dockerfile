# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install dependencies and Chromium
RUN apt-get update && \
    apt-get install -y wget unzip && \
    apt-get clean

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U selenium
RUN pip install webdriver-manager

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