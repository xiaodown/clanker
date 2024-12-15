# Clanker

Objective: discord bot that uses a LLM to chat with users

# Installation instructions
 * Check out the repo and cd into the directory.
 * Put OpenAI API key in openaiapikey.txt in the root of the checkout.
 * Put discord app api key in discordapikey.txt in the root of the checkout.
 * Install `uv` with `curl -LsSf https://astral.sh/uv/install.sh | sh`.
 * Use `uv` to install python 3.12:
 * * `uv python install 3.12`
 * Use `uv` to create a venv:
 * * `uv venv` (from the root of the checkout)
 * Activate the venv as instructed by uv.
 * Use `uv` to pip install the requirements:
 * * `uv pip install -r requirements.txt`

# Run instructions
Just run the run.sh script.

To debug the AI message/response, you can run chat.py standalone.

# Why is it called Clanker?
Clanker is a star wars term (kind of derogatory) for a worthless droid.
That's the bot's name in my discord server, but ofc it's configurable.

# TODO:
I eventually want:
 * Him to have something of a memory of what he's said
 * To not be using OpenAI, instead to use a LLM that I have some more control over and maybe host locally.
 * Eventually maybe even stream on twitch with a vtuber avatar like neuro-sama? 
 * * but probably not.  That seems like a lot of work.