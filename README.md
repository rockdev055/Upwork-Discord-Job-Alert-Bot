# Upwork Job Alert Bot

![Upwork Job Alert Bot](https://github.com/Zeeshanahmad4/Upwork-Discord-Job-Alert-Bot/blob/main/Screen%20Shot%202023-04-28%20at%209.58.22%20AM.png)

This is a Discord bot that fetches the latest jobs from an Upwork RSS feed and posts them in a designated Discord channel. The bot checks for new jobs every 2 minutes, and it can also be triggered manually using the `!checknow` command.

## Features

- Fetches job postings from an Upwork RSS feed
- Posts new jobs in a Discord channel
- Automatically checks for new jobs every 2 minutes
- Manual job checking with the `!checknow` command

## Setup

1. Clone this repository or download the source code
2. Install the required dependencies using pip:


`pip install -r requirements.txt` 

3. Replace the placeholders in the code with your Discord bot token, Upwork RSS feed URL, and Discord channel ID
4. Run the bot:

`python bot.py` 

## Commands

- `!checknow`: Manually check for new jobs
