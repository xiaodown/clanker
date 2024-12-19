import requests
import logging
import settings

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
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an error for bad status codes
    # print("\n *** RESPONSE: " + str(response.json()) + " *** \n")
    return AIResponse(response.json())

def upload_file(file_path):
    api_key = load_openwebui_key()
    url = 'http://localhost:8080/api/v1/files/'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, headers=headers, files=files)
    return response.json()

def add_chat_message_to_memory(message):
    # Kind of a generic method name because this may change
    message.