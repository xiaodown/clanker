import discord
import chat

with open('discordapikey.txt', 'r') as file:
    api_key = file.read().strip()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("Clanker is on " + str(guild_count) + " servers.")

@bot.event
async def on_message(message):
    print(f"Message from {message.author}: {message.content}")
    if message.content == "hello":
        await message.channel.send("hey dirtbag")
    if "clanker" in message.content.lower():
        await message.channel.send(chat.get_ai_response(message.content))
    
bot.run(api_key)