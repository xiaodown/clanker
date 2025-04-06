from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

import settings

# If you're using this file, it assumes you're using ollama. I 
# didn't make this work with OpenAI.  Possible in the future.


def get_response(prompt, model):
    # Create an instance of the OllamaLLM with the specified model
    llm = OllamaLLM(model=model)
    
    # Create a prompt template
    prompt_template = ChatPromptTemplate.from_template(prompt)
    
    # Chain the prompt with the model
    chain = prompt_template | llm
    
    # Invoke the chain with the prompt
    return chain.invoke({"question": prompt})
