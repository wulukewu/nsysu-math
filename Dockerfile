FROM ubuntu:latest

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
    curl \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxss1 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libxkbcommon-x11-0

# Get latest stable Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Get latest compatible ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    DRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | jq -r ".channels.Stable.version") && \
    DRIVER_PATH=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | jq -r ".channels.Stable.downloads.chromedriver[] | select(.platform==\"linux64\") | .url") && \
    wget -O /tmp/chromedriver.zip "$DRIVER_PATH" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

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