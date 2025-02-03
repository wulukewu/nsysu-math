# NSYSU Biweekly Math Problem Web Q&A

This Python script and GitHub Actions workflow automatically checks the NSYSU Biweekly Math Problem's website for new announcements and sends them to a specified Discord channel.

Website: [中山大學雙週一題網路數學問題徵答](https://www.math.nsysu.edu.tw/~problem/)

## Overview

The script uses:

-   **Selenium:** To scrape the NSYSU Math Department's website.
-   **Discord.py:** To send messages to a Discord channel.
-   **python-dotenv:** To load environment variables from a `.env` file.
-   **GitHub Actions:** To schedule the script to run automatically.
-   **Docker:** To package the application and its dependencies into a container.

## Prerequisites

Before using this script, you will need to have:

1.  **Python 3.12 or higher** installed on your system. (Note: Dockerfile uses 3.12 as base)
2.  **A Discord Bot Token:** You'll need to create a Discord application and bot and obtain its token.
3.  **Discord Guild ID:** The ID of the server where you want the bot to post messages.
4.  **Discord Channel ID:** The ID of the specific channel in the server where you want the bot to post messages.
5. **Docker** installed on your system (if you plan to use the Docker image)

## Setup

### 1. Clone the Repository

Clone this repository to your local machine.

```bash
git clone git@github.com:wulukewu/nsysu-math.git
cd nsysu-math
```

### 2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file in the root directory of your project and add the following variables:

```
DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
DISCORD_GUILD_ID="YOUR_DISCORD_GUILD_ID"
DISCORD_CHANNEL_ID="YOUR_DISCORD_CHANNEL_ID"
```

**Replace `YOUR_DISCORD_BOT_TOKEN`, `YOUR_DISCORD_GUILD_ID`, and `YOUR_DISCORD_CHANNEL_ID` with your actual values.**

### 4. Running Locally (Optional)

To test the script locally, run:

```bash
python main.py
```

**Make sure you have Chrome and ChromeDriver installed. You can download ChromeDriver from [here](https://chromedriver.chromium.org/downloads) and place it in a directory included in your PATH environment variable.**

## Docker Setup

This project includes a `Dockerfile` for building a Docker image to run the script in a containerized environment.

### 1. Building the Docker Image

To build the Docker image, navigate to the root directory of the project and run:

```bash
docker build -t nsysu-math .
```
This will create the docker image that contains all the dependencies.

### 2. Running the Docker Container

To run the Docker container, you will need to pass the Discord bot token, guild ID, and channel ID as build arguments during the build step or as environment variables at runtime. Example:

```bash
docker run --rm \
-e DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN" \
-e DISCORD_GUILD_ID=YOUR_DISCORD_GUILD_ID \
-e DISCORD_CHANNEL_ID=YOUR_DISCORD_CHANNEL_ID \
ghcr.io/YOUR_USERNAME/nsysu-math:latest
```

**Replace `YOUR_DISCORD_BOT_TOKEN`, `YOUR_DISCORD_GUILD_ID`, and `YOUR_DISCORD_CHANNEL_ID` with your actual values.**

This allows you to easily run the script in a consistent and isolated environment.

## GitHub Actions Setup

This repository includes a GitHub Actions workflow that automatically runs the script on a schedule.

### 1. Add Secrets to your GitHub Repository

-   Go to your GitHub repository's settings.
-   Navigate to "Secrets and variables" > "Actions".
-   Click "New repository secret".
-   Add the following secrets:
    -   `DISCORD_TOKEN`: Your Discord Bot Token.
    -   `DISCORD_GUILD_ID`: Your Discord Server (Guild) ID.
    -   `DISCORD_CHANNEL_ID`: Your Discord Channel ID.

### 2. Understand the GitHub Action (`run-crawler.yml`)

The GitHub Action file (`run-crawler.yml`) in the `.github/workflows` directory is configured to:

-   Run every day at 12:30 Taiwan Time (UTC+8), which translates to 04:30 UTC.
-   Checkout the code.
-   Set up Python 3.12.
-   Install dependencies from `requirements.txt`.
-   Execute `main.py`, making use of the GitHub secrets you have provided.

## How to Use

### Getting the Required IDs

#### 1. Discord Bot Token

-   Go to [Discord Developer Portal](https://discord.com/developers/applications).
-   Create a new Application.
-   Go to the "Bot" tab and click "Add Bot".
-   Copy the **Token** under the "Build-A-Bot" section.

#### 2. Discord Server (Guild) ID

-   In Discord, enable Developer Mode in Settings (User Settings > Advanced > Developer Mode).
-   Right-click on your server's icon and select "Copy ID".

#### 3. Discord Channel ID

-   In Discord, right-click on the desired channel and select "Copy ID".

### Getting and Setting on GitHub

1.  **Fork the Repository**
    Click the "Fork" button at the top right of this repository's page to create a copy of the repository in your GitHub account.
2.  **Add secrets**
    Follow the above steps to add secrets.
3.  **Enable Actions**
    Go to the 'Actions' tab on your forked repository.
    Click on the 'I understand my workflows, go ahead and enable them' button to enable GitHub Actions for your fork.
4.  **Monitor the Workflow**
    The workflow will automatically run based on the schedule specified in the yml file. You can check the workflow run history in the 'Actions' tab of your repository and see the log.

## Script Details

-   The script uses the specified environment variables to send the Discord message.
-   It scrapes the NSYSU math website table to check if there are any new announcements, based on the current Taiwan date.
-   If there are, it will format the message and send it to the Discord channel.
-   It sends only messages for the current date.

## Troubleshooting

-   **Script Not Running:**
    -   Check the GitHub Actions tab for any errors.
    -   Ensure that your GitHub secrets are correctly configured.
    -   Verify the cron schedule is correct for your needs.
    -   Make sure your GitHub Actions is enabled for the forked repository.
    -   If using Docker, ensure the container is running with the correct environment variables.
-   **Discord Bot Not Posting:**
    -   Ensure your bot has the correct permissions in the channel.
    -   Verify that the Discord bot token and the guild and channel ids are correct.
-   **Website Scraping Issues:**
    -   Verify the specified URL is still correct.
    -   Check the HTML structure of the page for changes which may require a change in the XPATH used for finding the table element.
    -   If you encounter any difficulties please create an issue in the repository with a description of the problem.
-   **Docker Issues**
    - Make sure that Docker is running correctly.
    - If using Docker, check that the image has been built successfully and the command to run it is correct with the necessary environmental variables.

## Contributing

If you would like to contribute to this project, please feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

-   **Running Selenium inside a Docker Container with GitHub Actions:** [Docker 建置打包 Python Selenium + Chromedriver + Chrome](https://medium.com/@hao66bmbm/docker-%E5%BB%BA%E7%BD%AE%E6%89%93%E5%8C%85-python-selenium-chromedriver-chrome-f74387266131)