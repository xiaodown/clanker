from enum import Enum

class AIProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    OPENWEBUI = "openwebui"

    def __str__(self):
        return self.value

class AI:
    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.model = self.get_model()

    def get_model(self):
        if self.provider == AIProvider.OPENAI:
            return "gpt-4o-mini"
        elif self.provider == AIProvider.OLLAMA:
            return "gemma2"
        elif self.provider == AIProvider.OPENWEBUI:
            return "dolphin-llama3:8b-256k"

def load_openai_api_key():
    try:
        with open('openaiapikey.txt', 'r') as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        return None

def load_discord_api_key():
    with open('discordapikey.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

def load_openwebui_api_key():
    with open('openwebuiapikey.txt', 'r') as file:
        api_key = file.read().strip()
    return api_key

# Changable settings below here

bot_name = "Clanker"
ai = AI(AIProvider.OPENWEBUI)  # Change this to switch providers