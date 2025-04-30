from datetime import datetime, timedelta
import asyncio
import bot_interface
import chat_handler
import discord
import logging
import random
import settings


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

bot_name = settings.bot_name
api_key = settings.load_discord_api_key()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

_last_message_time = datetime.now()
_bot_has_ever_spoken = False
_last_guild_id = 0
_last_channel_id = 0

# Global list to track channels where the bot has seen messages
# This is dirty - if the bot is not running at 9am it might miss a summarizing event.
_spoken_channels = set()

async def check_inactivity():
    # In theory, if the bot has spoken, but hasn't spoken for 2-3 hours, he will
    # say something in the last channel he spoke in.
    # God only knows if this will break, globals with async seems like inviting disaster.
    deltaminutes = (240 + random.randint(1, 59))
    await bot.wait_until_ready()
    global _last_message_time
    while not bot.is_closed():
        if _bot_has_ever_spoken:
            if datetime.now() - _last_message_time > timedelta(minutes=deltaminutes):
                print(f"Two hours, {deltaminutes - 120} minutes have passed without a message.")
                message = bot_interface.get_ai_idle_musing()
                guild = bot.get_guild(_last_guild_id)
                if guild:
                    channel = guild.get_channel(_last_channel_id)
                    if channel:
                        # reset delta to randomize it each time
                        deltaminutes = (240 + random.randint(1, 59))
                        await channel.send(message)
                # Reset the last_message_time to avoid doing it again immediately
                _last_message_time = datetime.now()
        await asyncio.sleep(60)  # Check every minute

async def save_longterm_chat():
    await bot.wait_until_ready()
    while not bot.is_closed():
        # Calculate the time until 9 AM
        now = datetime.now()
        next_run = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1, hours=9)
        if now.hour >= 9:
            next_run += timedelta(days=1)
        wait_time = (next_run - now).total_seconds()

        # Wait until 9 AM
        await asyncio.sleep(wait_time)

        # Iterate over all channels the bot has spoken in
        for channel_id in _spoken_channels:
            channel = bot.get_channel(channel_id)
            try:
                if channel and isinstance(channel, discord.TextChannel) and channel.name:
                    result = chat_handler.summarize_chat(channel.name)
                    if result and isinstance(result, str):
                        # I want to see this to know if it's working
                        await channel.send(result)
                    else:
                        print(f"Failed to summarize chat for channel: {channel.name}")
            except Exception as e:
                logger.error(f"Error summarizing chat for channel {channel_id}: {e}")
                print(f"Error summarizing chat for channel {channel_id}: {e}")

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print(f"{bot_name} is on " + str(guild_count) + " servers.")
    bot.loop.create_task(check_inactivity())
    bot.loop.create_task(save_longterm_chat())

@bot.event
async def on_message(message):
    # Last message time updated here to cover all channels the bot is in.
    # This means he'll only speak if the server is truely dead.
    # If he's on multiple servers, they'd all have to be dead - this is really 
    # meant to only be on one server for small group amusement.
    global _last_message_time
    _last_message_time = datetime.now()

    # Track the channel where the bot has spoken
    if message.channel.id not in _spoken_channels:
        _spoken_channels.add(message.channel.id)

    try:
        chat_handler.save_chat_message(message)
    except:
        logger.error("Failed to save chat message.")
        print("Failed to add chat message to memory.")

    print(f"Message from {message.author.name}: {message.content}")

    # Decide if the bot should respond based on settings
    should_talk = False
    if not settings.bot_decides_if_it_should_talk:
        # Use the simpler logic: check if the bot's name is mentioned
        if bot_name.lower() in message.content.lower() and message.author != bot.user:
            should_talk = True
    else:
        if message.author != bot.user:
            # Use the advanced (read: jank) logic: check if the bot is being addressed
            should_talk = bot_interface.is_bot_being_addressed(
                message.author.name, message.channel.name, message.content
            )

    # If the bot should talk, respond
    if should_talk and message.author != bot.user:
        global _bot_has_ever_spoken, _last_guild_id, _last_channel_id
        _bot_has_ever_spoken = True
        _last_guild_id = message.guild.id
        _last_channel_id = message.channel.id

        await message.channel.send(
            bot_interface.get_response(
                message.channel.name,
                message.author.name,
                message.content
            )
        )

bot.run(api_key)