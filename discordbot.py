import discord
import openai_bot_interface
import asyncio
from datetime import datetime, timedelta
import random

bot_name = "Clanker"

with open('discordapikey.txt', 'r') as file:
    api_key = file.read().strip()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

last_message_time = datetime.now()
bot_has_ever_spoken = False
last_guild_id = 0
last_channel_id = 0

async def check_inactivity():
    # In theory, if the bot has spoken, but hasn't spoken for 2-3 hours, he will
    # say something in the last channel he spoke in.
    # God only knows if this will break, globals with async seems like inviting disaster.
    deltaminutes = (120 + random.randint(1, 59))
    await bot.wait_until_ready()
    global last_message_time
    while not bot.is_closed():
        #print("Idle timer check")
        if bot_has_ever_spoken:
            if datetime.now() - last_message_time > timedelta(minutes=deltaminutes):
                print(f"Two hours and {deltaminutes - 120} minutes has passed without a message.")
                message = openai_bot_interface.get_ai_idle_musing()
                guild = bot.get_guild(last_guild_id)
                if guild:
                    channel = guild.get_channel(last_channel_id)
                    if channel:
                        # reset delta to randomize it each time
                        deltaminutes = (120 + random.randint(1, 59))
                        await channel.send(message)
                # Reset the last_message_time to avoid doing again immediately
                last_message_time = datetime.now()
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
    global last_message_time
    last_message_time = datetime.now()
    print(f"Message from {message.author}: {message.content}")
    if bot_name.lower() in message.content.lower() and message.author != bot.user:
        global bot_has_ever_spoken
        bot_has_ever_spoken = True
        global last_guild_id
        last_guild_id = message.guild.id
        global last_channel_id
        last_channel_id = message.channel.id
        await message.channel.send(openai_bot_interface.get_ai_response(message.content))

bot.run(api_key)