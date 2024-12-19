import discord
import bot_interface
import asyncio
from datetime import datetime, timedelta
import random
import settings
import interfaces.openwebui_interface as openwebui_interface

bot_name = settings.bot_name
api_key = settings.load_discord_api_key()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

_last_message_time = datetime.now()
_bot_has_ever_spoken = False
_last_guild_id = 0
_last_channel_id = 0

async def check_inactivity():
    # In theory, if the bot has spoken, but hasn't spoken for 2-3 hours, he will
    # say something in the last channel he spoke in.
    # God only knows if this will break, globals with async seems like inviting disaster.
    deltaminutes = (120 + random.randint(1, 59))
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
                        deltaminutes = (120 + random.randint(1, 59))
                        await channel.send(message)
                # Reset the last_message_time to avoid doing again immediately
                _last_message_time = datetime.now()
        await asyncio.sleep(60)  # Check every minute

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print(f"{bot_name} is on " + str(guild_count) + " servers.")
    bot.loop.create_task(check_inactivity())

@bot.event
async def on_message(message):
    # Last message time updated here to cover all channels the bot is in.
    # This means he'll only speak if the server is truely dead.
    # If he's on multiple servers, they'd all have to be dead - this is really 
    # meant to only be on one server for small group amusement.
    global _last_message_time
    _last_message_time = datetime.now()
    openwebui_interface.add_chat_message_to_memory(message)
    print(f"Message from {message.author}: {message.content}")
    if bot_name.lower() in message.content.lower() and message.author != bot.user:
        global _bot_has_ever_spoken
        _bot_has_ever_spoken = True
        global _last_guild_id
        _last_guild_id = message.guild.id
        global _last_channel_id
        _last_channel_id = message.channel.id
        await message.channel.send(bot_interface.get_ai_response(message.content))

bot.run(api_key)