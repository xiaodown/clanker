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
            #return "dolphin-llama3:8b-256k"
            return "gemma2:latest"

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
bypass_filter = True # only applies to open-webui interface


# Below is the knowledge_id of the knowledge collection.  This is what
# allows for RAG / basically for the model to use chat logs for context.
# Everything said in any chat that the bot is in will be stored here.
# You can create a knowledge collection by using a curl command similar
# to the one below.  You'll need the id, which is the first field returned.
# For now, this must be done manually.  
# Only applies to open-webui interface.
'''
curl -X 'POST' \
  'http://localhost:8080/api/v1/knowledge/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "kb_name",
  "description": "Your Description",
  "data": {},
  "access_control": {}
}'
'''
knowledge_id = "f3359da7-3438-4d02-9b2b-5045d9e32fe6"