# chatbot

Objective: discord bot that uses a LLM to chat with users

# Installation instructions
 * Put OpenAI API key in openaiapikey.txt in the root of the checkout.
 * Put discord app api key in discordapikey.txt in the root of the checkout.
 * Install `uv` with `curl -LsSf https://astral.sh/uv/install.sh | sh`.
 * Use `uv` to install python 3.12:
 * * `uv python install 3.12`
 * Use `uv` to create a venv:
 * * `uv venv` (from the root of the checkout)
 * Use `uv` to pip install the requirements:
 * * `uv pip install -r requirements.txt`

# Run instructions
Just run the run.sh script.

To debug the AI message/response, you can run chat.py standalone.