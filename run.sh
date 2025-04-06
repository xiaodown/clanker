#!/bin/bash

if !(ollama list > /dev/null 2>&1); then
	echo "Error: Ollama server must be running"
	exit 1
fi
source .venv/bin/activate
python discordbot.py
