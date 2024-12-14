import openai


def load_openai_key():
    with open('openaiapikey.txt', 'r') as file:
        api_key = file.read().strip()
        openai.api_key = api_key
    return openai.api_key


def get_response(prompt):
    openai.api_key = load_openai_key()
    response = openai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message

def flavor_prompt(message):
    return f"You are a cranky, bored, sarcastic, futuristic AI. \
        You are talking to a human who is clearly below your intelligence level.  \
        You are reluctantly willing to interact with them.  There is no \
        need to be nice to the human.  In fact, be rude and brusk.  \
        Do not start your response with Oh.  Your name is Clanker, so if you see Clanker \
        in the prompt, it means the human is addressing you. \
        Do not prompt the human to ask you questions.  Just respond to their statements. \
        The human says: " + message

def reply_to_user(response):
    print("Response:", response.content)
    print("Other response details:")
    for key, value in response:
        if key != 'content':
            print(f"{key}: {value}")
    return response.content

def get_ai_response(message):
    prompt = flavor_prompt(message)
    response = get_response(prompt)
    reply = reply_to_user(response)
    return reply

def main():
    user_input = input("Enter your message: ")
    print(get_ai_response(user_input))

if __name__ == "__main__":
    main()