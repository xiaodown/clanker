import openai

# Read the API key from the file
with open('openaiapikey.txt', 'r') as file:
    api_key = file.read().strip()

# Set the API key
openai.api_key = api_key

def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']

def main():
    user_input = input("Enter your message: ")
    embedding = get_embedding(user_input)
    print("Embedding:", embedding)

if __name__ == "__main__":
    main()