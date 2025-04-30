import os
import json
import logging
from datetime import datetime, timedelta
import bot_interface
from settings import bot_name

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)



def save_chat_message(message):
    channel = message.channel.name
    author = message.author.name
    content = message.content
    timestamp = message.created_at.strftime("%B %d, %Y, %I:%M:%S %p")

    os.makedirs('chat_logs', exist_ok=True)
    os.makedirs('chat_logs/short_term', exist_ok=True)
    os.makedirs('chat_logs/long_term', exist_ok=True)
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

def summarize_from_string(chatlog) -> str:
    """
    Takes any string and sends it to the LLM for summarization.
    In the event of failure, it returns a falsy value.
    """    
    prompt = (
        "Summarize the following chat logs:\n\n"
        f"{chatlog}\n\n"
        "Provide a concise summary, but don't miss important discussion topics\n"
        "any significant events that occurred during the conversation, and who"
        "said what."
    )

    try:
        response = bot_interface.get_raw_response(prompt)
        summary = response['choices'][0]['message']['content']
        return summary
    except Exception as e:
        logger.error("Error getting response from Ollama: %s", e)
        return ""

def summarize_chat(channel) -> str:
    # Calculate yesterday's date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    short_term_file = f'chat_logs/short_term/{channel}_{yesterday}.json'
    long_term_file = f'chat_logs/long_term/{channel}_{yesterday}.txt'

    # Check if the summary already exists in long_term
    if os.path.exists(long_term_file):
        logger.info("Summary for %s already exists in long_term.", yesterday)
        return False

    # Check if the short_term file exists
    if not os.path.exists(short_term_file):
        logger.info("No chat logs found for %s in short_term.", yesterday)
        return "No chat logs found for %s in short_term.", yesterday

    # Load the short_term file
    try:
        with open(short_term_file, 'r') as file:
            chat_logs = json.load(file)
    except json.JSONDecodeError:
        logger.error("Error decoding JSON data in %s", short_term_file)
        return False

    # Convert chat logs to a human-readable string
    readable_logs = ""
    for log in chat_logs:
        readable_logs += f"[{log['timestamp']}] {log['speaker']}: {log['content']}\n"

    summary = summarize_from_string(readable_logs)

    # Save the summary to the long_term directory
    os.makedirs('chat_logs/long_term', exist_ok=True)
    with open(long_term_file, 'w') as file:
        file.write(summary)

    logger.info("Summary for %s saved to %s.", yesterday, long_term_file)
    return "Summary for %s saved to %s.", yesterday, long_term_file


def get_current_day_logs(channel):
    filename = f'chat_logs/short_term/{channel}_{datetime.now().strftime("%Y-%m-%d")}.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                # Convert JSON data to a human-readable string
                readable_logs = ""

                for log in data:
                    # Parse the timestamp and extract only the time
                    timestamp = datetime.strptime(log['timestamp'], "%B %d, %Y, %I:%M:%S %p").strftime("%I:%M:%S %p")
                    # Strip out newlines from log['content']
                    content = log['content'].replace("\n", " ")
                    readable_logs += f"[{timestamp}] {log['speaker']}: {content}\n"
                                # Split logs into lines

                log_lines = readable_logs.splitlines()
                if len(log_lines) > 20:
                    last_20_lines = "\n".join(log_lines[-20:])
                    earlier_logs = "\n".join(log_lines[:-20])
                    summary = summarize_from_string(earlier_logs)
                    print(f"Summary because logs were too long: \n {summary}")
                    combined_logs = f"{summary}\n\n{last_20_lines}"
                    return combined_logs
                else:
                    return readable_logs
                
            except json.JSONDecodeError:
                logger.error("Error decoding JSON data.")
            except Exception as e:
                logger.error("Unknown error: %s", e)
                print(f"Unknown error: ", e)
    else:
        return ""

def get_long_term_logs(channel):
    logs = []
    for i in range(1, 5):  # Loop for the last 4 days (yesterday and 3 days before)
        day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        filename = f'chat_logs/long_term/{channel}_{day}.txt'
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    logs.append(file.read())
            except Exception as e:
                logger.error("Error reading log: %s", e)
        else:
            logger.info("No logs found for %s.", day)
    
    if not any(logs):
        return None
    return "\n\n".join(logs)