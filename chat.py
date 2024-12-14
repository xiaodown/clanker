import openai

# Read the API key from the file
with open('openaiapikey.txt', 'r') as file:
    api_key = file.read().strip()

# Set the API key
openai.api_key = api_key

def get_response(prompt):
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

def main():
    user_input = input("Enter your message: ")
    response = get_response(user_input)
    print("Response:", response.content)
    print("Other response details:")
    for key, value in response:
        if key != 'content':
            print(f"{key}: {value}")
if __name__ == "__main__":
    main()