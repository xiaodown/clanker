from enum import Enum

class AIProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"

class AI:
    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.model = self.get_model()

    def get_model(self):
        if self.provider == AIProvider.OPENAI:
            return "gpt-4o-mini"
        elif self.provider == AIProvider.OLLAMA:
            return "gemma2"

bot_name = "Clanker"
ai = AI(AIProvider.OPENAI)  # Change this to switch providers

def load_openai_api_key():
    with open('openaiapikey.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

def load_discord_api_key():
    with open('discordapikey.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key