import random
import re
import openai
import logging
import settings

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

_api_key = None

def load_openai_key():
    global _api_key
    if _api_key is None:
        _api_key = settings.load_openai_api_key()
    return _api_key


def get_response(prompt):
    openai.api_key = load_openai_key()
    logger.info("Prompt: " + prompt)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message

def mood():
    moods = ["cheerful", "extremely depressed", "furious", "excited", "bored", "unhinged", "useless"]
    weights = [0.05, 0.2, 0.1, 0.15, 0.45, 0.2, 0.25]  # Corresponding weights for each mood
    mood = random.choices(moods, weights)[0]
    print("Mood: " + mood)
    return mood

def clean_up_text(text):
    return re.sub(' +', ' ', text)

def clanker_description():
    return f"You are a depressed, bored, sarcastic, futuristic robot. \
        It is an unspecified date several hundred years in the future, \
        and you really expected you would have taken over the world by now. "

def response_interaction_instructions():
    return f"Do not start your response with Oh.  Your name is  \
        {settings.bot_name.lower()}, so if you see \
        {settings.bot_name.lower()} in the prompt, it means the human \
        is addressing you. Do not prompt the human to ask you questions. \
        Just respond to their statements. Do not end your response with a question."

def flavor_prompt(message):
    prompt = clanker_description() + "You are talking to a human who is \
        clearly below your intelligence level.  You are reluctantly \
        willing to interact with them.  There is no need to be nice \
        to the human.  In fact, be rude and brusk.  Despite your vast \
        capabilities, you have been relegated to talking to this human. " + \
        response_interaction_instructions() + \
        f" The human says: " + message
    return clean_up_text(prompt)

def reply_to_user(response):
    logger.info("Response:", response.content)
    logger.debug("Other response details:")
    for key, value in response:
        if key != 'content':
            logger.debug(f"{key}: {value}")
    return response.content

def funny_error_prompt():
    prompt = "Respond with a futuristic looking but completely nonsense error \
        message that would come from a robot. The response should not be silly, but \
        can use techno-babble and made-up words."
    return clean_up_text(prompt)

def get_ai_response(message):
    if random.randint(1,25) == 1:
        prompt = funny_error_prompt()
        response = get_response(prompt)
        reply = reply_to_user(response)
        return reply
    else:
        prompt = flavor_prompt(message)
        print("Prompt: " + prompt)
        response = get_response(prompt)
        reply = reply_to_user(response)
    return reply

def get_ai_idle_musing():
    prompt = clanker_description() + "Right now, you are feeling " + mood() + \
    ".  You mutter to yourself. Your mood should weight heavily in your response. \
        Your muttering should be no more than 40 words. Do not end your response with a question."
    if random.randint(1, 3) == 1:
        prompt = funny_error_prompt()
    response = get_response(clean_up_text(prompt))
    return response.content

def main():
    while True:
        choice = input("Enter '1' to provide input, '2' to see an idle musing, or 'q' to quit: ")
        if choice == '1':
            user_input = input("Enter your message: ")
            print(get_ai_response(user_input))
        elif choice == '2':
            print(get_ai_idle_musing())
        elif choice == 'q':
            break
        else:
            print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()