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


def get_response(prompt, model):
    openai.api_key = load_openai_key()
    logger.info("Prompt: " + prompt)
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message