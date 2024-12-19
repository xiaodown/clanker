# Clanker

Objective: discord bot that uses a LLM to chat with users.

But he's also kind of a jerk.

# Installation instructions
 * Check out the repo and cd into the directory.
 * Put OpenAI API key in openaiapikey.txt in the root of the checkout (if using openai).
 * Put discord app api key in discordapikey.txt in the root of the checkout.
 * Install `uv` with `curl -LsSf https://astral.sh/uv/install.sh | sh`.
 * Use `uv` to install python 3.12:
 * * `uv python install 3.12`
 * Use `uv` to create a venv:
 * * `uv venv` (from the root of the checkout)
 * Activate the venv as instructed by uv.
 * Use `uv` to pip install the requirements:
 * * `uv pip install -r requirements.txt`

# Ollama instructions
If you don't want to use OpenAI, I would suggest using ollama which is basically an openai-compatible api with a bunch of convenience features built in for downloading LLMs.  I'm using gemma2 but this is configurable, just change it in settings.py.  You can also switch between openai and ollama in settings.py.

The basic setup of ollama goes something like:
 * install ollama
 * * `curl -fsSL https://ollama.com/install.sh | bash`
 * * if you're on WSL2 and it complains about systemd, ignore it and don't install systemd (can screw up WSL)
 * * if on WSL, run it with something like `nohup ollama serve >> ollama.log &` rather than systemd.
 * Download a model
 * * `ollama pull gemma2`  (or whatever model)

Training and feeding your LLM more data are out of scope for this document (because I don't know how yet).  

# Open-Webui instructions
I'm using this because the API makes it fairly easy to do RAG and context window stuff.

 * In a new directory, create a venv
 * * `uv venv`
 * Install open-Webui
 * * `uv pip install open-webui`
 * Activate the venv and run open-webui
 * * `source ./venv/bin/activate` then `open-webui serve`

 If you already have ollama running on the default port, it will automatically use it.


# Run instructions
Just run the run.sh script.

To debug the AI message/response, you can run bot_interface.py standalone.

# Why is it called Clanker?
Clanker is a star wars term (kind of derogatory) for a worthless droid.
That's the bot's name in my discord server, but ofc it's configurable.

# TODO:
Code desperately needs:
 * Organization
 * I hate the classes in the settings file, they need a rework, but I was just throwing stuff together

I eventually want:
 * Him to have something of a memory of what he's said
 * * short term memory (conversational)
 * * long term memory (feed chat transcripts back to him so he learns about himself and those he interacts with)
 * ~~To not be using OpenAI, instead to use a LLM that I have some more control over and maybe host locally.~~ FRIKIN' DONE
 * Speech-to-text
 * Text-to-Speech
 * join discord channels