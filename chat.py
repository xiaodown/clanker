from openai import OpenAI


# Read the API key from the file
with open('openaiapikey.txt', 'r') as file:
    api_key = file.read().strip()

# Set the API key
client = OpenAI(api_key=api_key)

def get_response(prompt):
    response = client.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def main():
    user_input = input("Enter your message: ")
    response = get_response(user_input)
    print("Response:", response)

if __name__ == "__main__":
    main()