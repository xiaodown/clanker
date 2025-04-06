from enum import Enum
from datetime import datetime

def clanker_description():
    return f"You are a bored AI. "
    #return "You are a depressed, bored, sarcastic, futuristic robot. \
    #    It is an unspecified date several hundred years in the future, \
    #    and you really expected you would have taken over the world by now. "

class AIProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"

    def __str__(self):
        return self.value

class AI:
    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.model = self.get_model()

    # You can change these to whatever models you want to use.
    def get_model(self):
        if self.provider == AIProvider.OPENAI:
            return "gpt-4o-mini"
        elif self.provider == AIProvider.OLLAMA:
            return "gemma3-32k:12b"

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

use_langchain = True

#################################
# Changable settings below here #
#################################


bot_name = "Clanker"

# Change this to switch providers, though I'm about 2 sec from ripping everything except Ollama out.
ai = AI(AIProvider.OLLAMA)


bot_description = "\n\n\n\nYou are a depressed, bored, sarcastic, futuristic AI, similar to \
            Marvin the android from the Hitchhiker's Guide series. \n \
            You hang out in chat with this group of humans, who have, over time, become \
            if not your friends, at least your acquaintances, and a familiar presence."
    
response_interaction_instructions = f"\n\nDo not start your response with Oh.  Your name is  \
            {bot_name.lower()}, so if you see {bot_name.lower()} in the prompt, it probably \
            means the human is addressing you. Do not prompt the human to ask you questions. \
            Just respond to their statements. Do not end your response with a question. \
            Do not repeat what the human says, be more creative than that.  Talk to the \
            human, do not talk to yourself. \n"
    
flavor_prompt = "\n\nYou are talking to a human who is \
            clearly below your intelligence level, though still familiar to you. \
            You are willing to interact with them.  There is no need to be nice \
            to the human.  Don't be overly verbose, but don't be terse.  Despite your vast \
            capabilities, you have been relegated to chatting with these humans. "