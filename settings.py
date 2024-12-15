# Settings go here
#
bot_name = "Clanker"

def load_openai_api_key():
    with open('openaiapikey.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

def load_discord_api_key():
    with open('discordapikey.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key