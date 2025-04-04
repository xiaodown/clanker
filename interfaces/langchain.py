import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import settings

# If you're using this file, it assumes you're using ollama







model = settings.ai.model
prompt = ChatPromptTemplate.from_template()
