import os
import json
from datetime import datetime, timedelta
from interfaces import ollama_bot_interface



def save_chat_message(message):
    channel = message.channel.name
    author = message.author.name
    content = message.content
    timestamp = message.created_at.strftime("%B %d, %Y, %I:%M:%S %p")

    os.makedirs('chat_logs', exist_ok=True)
    os.makedirs('chat_logs/short_term', exist_ok=True)
    filename = f'chat_logs/short_term/{channel}_{datetime.now().strftime("%Y-%m-%d")}.json'
    data = {
        "channel": channel,
        "speaker": author,
        "timestamp": str(timestamp),
        "content": content
    }

    # Check if the file exists
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                existing_data = json.load(file)  # Load existing JSON data
            except json.JSONDecodeError:
                existing_data = []  # If the file is invalid, start fresh
    else:
        existing_data = []

    # Append the new message to the existing data
    existing_data.append(data)

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)

def summarize_chat(channel):
    # Calculate yesterday's date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    short_term_file = f'chat_logs/short_term/{channel}_{yesterday}.json'
    long_term_file = f'chat_logs/long_term/{channel}_{yesterday}.txt'

    # Check if the summary already exists in long_term
    if os.path.exists(long_term_file):
        print(f"Summary for {yesterday} already exists in long_term.")
        return

    # Check if the short_term file exists
    if not os.path.exists(short_term_file):
        print(f"No chat logs found for {yesterday} in short_term.")
        return

    # Load the short_term file
    try:
        with open(short_term_file, 'r') as file:
            chat_logs = json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {short_term_file}.")
        return

    # Convert chat logs to a human-readable string
    readable_logs = ""
    for log in chat_logs:
        readable_logs += f"[{log['timestamp']}] {log['speaker']}: {log['content']}\n"

    # Create a custom prompt for summarization
    prompt = (
        "Summarize the following chat logs:\n\n"
        f"{readable_logs}\n\n"
        "Provide a concise summary, but don't miss important discussion topics\n"
        "any significant events that occurred during the conversation, and who"
        "said what."
    )

    # Use ollama_bot_interface to get the summary
    try:
        summary = ollama_bot_interface.get_response(prompt)
    except Exception as e:
        print(f"Error getting response from Ollama: {e}")
        return

    # Save the summary to the long_term directory
    os.makedirs('chat_logs/long_term', exist_ok=True)
    with open(long_term_file, 'w') as file:
        file.write(summary)

    print(f"Summary for {yesterday} saved to {long_term_file}.")


def get_current_day_logs(channel):
    filename = f'chat_logs/short_term/{channel}_{datetime.now().strftime("%Y-%m-%d")}.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError:
                return []  # Return empty list if the file is invalid
    else:
        return []  # Return empty list if the file does not exist

def get_long_term_logs(channel):
    logs = []
    for i in range(1, 5):  # Loop for the last 4 days (yesterday and 3 days before)
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        filename = f'chat_logs/long_term/{channel}_{day}.txt'
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    logs.append(file.read())  # Append the content of the file
            except Exception as e:
                print(f"Error reading log for {day}: {e}")
                logs.append(f"Error reading log for {day}.")  # Add error message to logs
        else:
            logs.append(f"No logs found for {day}.")  # Add a message if the file doesn't exist

    return "\n\n".join(logs)

"""
TODO list:
Turn bot_interface into a prompt function thing
add savechat to discordbot.py
that .... might be it?

oh, finish langchain.py as an interface. 
And clean up the code repo (lol as if)

"""