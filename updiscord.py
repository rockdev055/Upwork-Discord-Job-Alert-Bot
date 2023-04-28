import os
import discord
from discord.ext import commands, tasks
import feedparser
import http.client
from datetime import datetime, timedelta
import pytz
import ssl

# Replace 'YOUR_BOT_TOKEN' with your Discord bot token
TOKEN = 'MTEwMDI5MTEzMzQzNjg2MjQ2NA.GmrSHw.rVDu3__L4KVJ7L3jYAlh6YglRhQN966UdgdxnY'

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Replace the URL with the Upwork RSS feed you provided
UPWORK_RSS_URL = 'https://www.upwork.com/ab/feed/jobs/rss?sort=recency&paging=0%3B50&api_params=1&q=&securityToken=25aaba64163c4fe3ce18573e9e3c6e839bcdf89ca6c13eb5e58db069b2e0c3740785ed51594f7a35d56d4bd5bc6d6b79901aaf4d1f6fd9e4a780868d53093351&userUid=1149214708548202496&orgUid=1149214708552396801'


def fetch_feed():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connection = http.client.HTTPSConnection("www.upwork.com", context=ctx)
    connection.request("GET", UPWORK_RSS_URL)

    response = connection.getresponse()
    xml_data = response.read().decode("utf-8")
    return feedparser.parse(xml_data)


seen_jobs = {entry.id for entry in fetch_feed().entries}


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_new_jobs.start()


@tasks.loop(minutes=2)
async def check_new_jobs():
    # Replace 'YOUR_CHANNEL_ID' with the ID of the channel where you want to receive notifications
    channel = bot.get_channel(1100293743699034152)
    if not channel:
        return

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connection = http.client.HTTPSConnection("www.upwork.com", context=ctx)
    connection.request("GET", UPWORK_RSS_URL)

    response = connection.getresponse()
    xml_data = response.read().decode("utf-8")
    feed = feedparser.parse(xml_data)

    # Set the timezone you want to use
    timezone = pytz.timezone("UTC")
    print(timezone)

    # Get the current time in the specified timezone
    now = datetime.now(timezone)

    for entry in reversed(feed.entries):
        # Parse the published time of the job
        published_time = datetime.strptime(
            entry.published, "%a, %d %b %Y %H:%M:%S %z")

        # Check if the job is published within the last 5 minutes
        if now - published_time <= timedelta(minutes=5):
            if entry.id not in seen_jobs:
                seen_jobs.add(entry.id)
                content = f"**New job posted:** {entry.title}\n{entry.link}"
                await channel.send(content)
    print("Checked for new jobs. No jobs found within the last minute.")


@bot.command(name='checknow', help='Manually check for new jobs')
async def manual_check(ctx):
    await check_new_jobs()

bot.run(TOKEN)
