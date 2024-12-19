# Clanker

Objective: discord bot that uses a LLM to chat with users.

But he's also kind of a jerk.

# Installation instructions
 * Check out the repo and cd into the directory.
 * Put OpenAI API key in openaiapikey.txt in the root of the checkout (if using openai).
 * Put discord app api key in discordapikey.txt in the root of the checkout.
 * (eventually, see below) put your open-webui api key into openwebuiapikey.txt
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
 * * `ollama pull gemma2`  (or whatever model, configurable in settings)

Training and feeding your LLM more data are out of scope for this document (because I don't know how yet).  

# Open-Webui instructions
I'm using this because the API makes it fairly easy to do RAG and context window stuff.

 * In a new directory, create a venv
 * * `uv venv`
 * Install open-Webui
 * * `uv pip install open-webui`
 * Activate the venv and run open-webui
 * * `source ./venv/bin/activate` then `open-webui serve`
 * Visit http://localhost:8080 and generate your api key
 * * click your name (lower left), Account, generate API key
 * * put this in openwebuiapikey.txt as instructed above

 If you already have ollama running on the default port, it will automatically use it.


# Run instructions
Just run the run.sh script.

To debug the AI message/response, you can run bot_interface.py standalone.

# Why is it called Clanker?
Clanker is a star wars term (kind of derogatory) for a worthless droid.
That's the bot's name in my discord server, but ofc it's configurable.

# TODO:
Code short term needs:
 * Organization
 * I hate the classes in the settings file, they need a rework, but I was just throwing stuff together
 * Create the knowledge collection if it doesn't exist, otherwise just use it.
 * Use the conversation function (right now basically everything is a new convo). 
 * * It could be something like start a convo, then once the same timer for the idle musing is up, end the convo (?)
 * Make him respond to DMs (currently it errors because message.guild.id doesn't make sense in a dm)
 * Find out why gemma2 doesn't like using the provided knowledge collection?

I eventually want:
 * Him to have something of a memory of what he's said
 * * short term memory (conversational)
 * * long term memory (feed chat transcripts back to him so he learns about himself and those he interacts with)
 * ~~To not be using OpenAI, instead to use a LLM that I have some more control over and maybe host locally.~~ FRIKIN' DONE
 * Speech-to-text
 * Text-to-Speech
 * join discord channels