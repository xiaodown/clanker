import random
import re
import logging
import settings
import interfaces.openai_bot_interface as openai_bot_interface
import interfaces.ollama_bot_interface as ollama_bot_interface
import interfaces.langchain as langchain_interface
from prompt import get_prompt
from chat_handler import get_current_day_logs

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def get_response(channel, speaker, message):
    print (f"using provider {settings.ai.provider} and model {settings.ai.model}")
    prompt = get_prompt(channel, speaker, message)

    if settings.use_langchain:
        return langchain_interface.get_response(prompt, model=settings.ai.model)
    # If we are not using langchain, use the provider directly
    if settings.ai.provider == settings.AIProvider.OPENAI:
        return openai_bot_interface.get_response(prompt, model=settings.ai.model)
    elif settings.ai.provider == settings.AIProvider.OLLAMA:
        return ollama_bot_interface.get_response(prompt, model=settings.ai.model)

def get_raw_response(prompt):
    if settings.ai.provider == settings.AIProvider.OPENAI:
        return openai_bot_interface.get_response(prompt, model=settings.ai.model)
    elif settings.ai.provider == settings.AIProvider.OLLAMA:
        return ollama_bot_interface.get_response(prompt, model=settings.ai.model)

def get_fast_raw_response(prompt):
    # So far, I haven't gotten this to work, running two models seems to really
    # not be possible, at least on my 3090ti.
    if settings.ai.provider == settings.AIProvider.OPENAI:
        return openai_bot_interface.get_response(prompt, model=settings.ai.fast_raw_model)
    elif settings.ai.provider == settings.AIProvider.OLLAMA:
        return ollama_bot_interface.get_response(prompt, model=settings.ai.fast_raw_model)
    
def is_bot_being_addressed(speaker, channel, message):
    # This ... lol doens't work great.  The bot thinks he should answer to everything.
    # what an ego.
    bot_being_addressed = False
    prompt = "Here is the recent conversation history: \n"
    full_logs = get_current_day_logs(channel)
    last_ten_lines = "\n".join(full_logs.splitlines()[-10:])
    prompt += last_ten_lines
    prompt += f"\n\n New chat message:  {speaker} said: {message}"
    prompt += f"\n\n Based on the conversation history and this new message, would \
              a human reply to the new message? if the new message is addressed to \
              {settings.bot_name} or 'the bot' or similar titles, then the likelihood of a \
              response is near certain. \n \
              If it appears the humans are only conversing between themselves, then this \
              is less likely, but still possible as a human would interject information if \
              it were relevant to the topic at hand.\n \
              Answer ONLY with 'True' or 'False'.\n Your answer must ONLY be 'True' or 'False'.\
              Do not add any other text. \n \
              You want the conversation to flow naturally, and avoid awkwardness. \n \
              In many cases, this means that you should not respond to the humans. \
              Consider the implications of your response: if you say 'True', then the bot \
              will respond in the channel.  If you say 'False', then the bot will not respond. \
              If you reply when you should not, or when a human would not reply, then it will \
              be awkward for you and more so for the humans.  \n \
              If you do not reply when you should, or when a human would reply, then it will \
              be awkward for you and more so for the humans.  \n \
              Remember, ONLY reply with False or True, and do not add any other text. \n \
              Bias towards not replying (False) if there is any ambiguity."

    prompt = re.sub(r'\t+', ' ', prompt)
    prompt = re.sub(r' {2,}', ' ', prompt)
    bot_being_addressed_response = get_raw_response(prompt).content
    if "true" in bot_being_addressed_response.lower():
        bot_being_addressed = True
    print(f"bot_being_addressed: {bot_being_addressed}")
    logger.info("bot_being_addressed: " + str(bot_being_addressed))
    return bool(bot_being_addressed)

def mood():
    moods = ["cheerful", "extremely depressed", "furious", "excited", "bored", "unhinged", "useless"]
    weights = [0.05, 0.2, 0.1, 0.15, 0.45, 0.2, 0.25]  # Corresponding weights for each mood
    mood = random.choices(moods, weights)[0]
    print("Mood: " + mood)
    return mood

def clean_up_text(text):
    return re.sub(' +', ' ', text)

def funny_error_prompt():
    # maybe fix this in the future
    pass
    #prompt = "Respond with a futuristic looking but completely nonsense error \
    #    message that would come from a robot. The response should not be silly, but \
    #    can use techno-babble and made-up words."
    #return clean_up_text(prompt)

def get_ai_idle_musing():
    # maybe fix this in the future
    pass
    #prompt = clanker_description() + "Right now, you are feeling " + mood() + \
    #".  You mutter to yourself. Your mood should weight heavily in your response. \
    #    Your muttering should be no more than 40 words. Do not end your response with a question, \
    #    unless it is rhetorical.  Do not surround your answer with quotation marks.  Do not\
    #    use quotation marks in your response.  "
    #if random.randint(1, 5) == 1:
    #    prompt = funny_error_prompt()
    #response = get_response(clean_up_text(prompt))
    #return response.content