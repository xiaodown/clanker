import openai
import logging
import settings

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


client = openai.OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

def get_response(prompt, model=settings.AI.get_model):
    logger.info("Prompt: " + prompt)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message