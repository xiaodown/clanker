import requests
import logging
import settings
import os
from datetime import datetime

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


base_url = 'http://localhost:8080/'
_api_key = None

def load_openwebui_key():
    global _api_key
    if _api_key is None:
        _api_key = settings.load_openwebui_api_key()
    return _api_key

class AIResponse:
    # They say open-webui is openai compatible, but then I have to do this. Sigh.
    def __init__(self, response_dict):
        self.id = response_dict.get('id')
        self.created = response_dict.get('created')
        self.model = response_dict.get('model')
        self.choices = response_dict.get('choices')
        self.object = response_dict.get('object')
        self.content = response_dict['choices'][0]['message']['content']

def get_response(prompt, model):
    logger.info("Prompt: " + prompt)
    api_key = load_openwebui_key()
    url = f"{base_url}api/chat/completions?bypass_filter={settings.bypass_filter}"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model,
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'files': [{'type': 'collection', 'id': settings.knowledge_id}]
    }
    print(f"Data: {data}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        logger.error(f"Response status code: {response.status_code}")
        logger.error(f"Response content: {response.content}")
        raise
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
    return AIResponse(response.json())


def save_chat_message(message):
    channel = message.channel.name
    author = message.author.name
    content = message.content
    timestamp = message.created_at

    os.makedirs('chat_logs', exist_ok=True)
    filename = f'chat_logs/{channel}_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.txt'
    with open(filename, 'w') as file:
        file.write(f"channel = {channel}\n")
        file.write(f"author = {author}\n")
        file.write(f"timestamp = {timestamp}\n")
        file.write(f"content = {content}\n")
    return filename


def upload_file(file_path):
    api_key = load_openwebui_key()
    url = 'http://localhost:8080/api/v1/files/'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, headers=headers, files=files)
    response_data = response.json()
    return response_data.get('id')

def remove_uploaded_file(file_path):
    os.remove(file_path)

def add_file_to_primary_kb(file_id):
    api_key = load_openwebui_key()
    url = f'http://localhost:8080/api/v1/knowledge/{settings.knowledge_id}/file/add'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {'file_id': file_id}
    response = requests.post(url, headers=headers, json=data)

def add_chat_message_to_memory(message):
    # Kind of a generic method name because this may change
    print(f"Adding chat message from {message.author} to memory.")
    filename = save_chat_message(message)
    file_id = upload_file(filename)
    add_file_to_primary_kb(file_id)
    remove_uploaded_file(filename)

