import settings
from datetime import datetime
from chat_handler import get_current_day_logs, get_long_term_logs
import re
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def add_short_term_context(channel):
    stc = get_current_day_logs(channel)
    if stc:
        context = "\n\nHere is today's conversation history: \n"
        context += stc
        return context
    else:
        return ""
    
def add_long_term_context(channel):
    ltc = get_long_term_logs(channel)
    if ltc:  # Check if ltc is not None or empty
        context = "\n\nHere is a summary of the last few days of conversation history: \n"
        context += ltc
        return context
    else:
        return ""


def get_human_readable_date():
    now = datetime.now()
    day = now.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return now.strftime(f"%B {day}{suffix}, %Y")

def get_basic_parameters():
    return f"You chat with humans.  Your name is {settings.bot_name}.\n \
            Today's date is {get_human_readable_date()}.\n"


def get_prompt(channel, speaker, message):
    context_line_length = 25
    prompt = ""
    prompt += get_basic_parameters()
    prompt += f"\nHere is the recent conversation history: \n"
    # prompt += add_short_term_context(channel)
    # the whole daily conversation is too long for the context window :(
    full_logs = add_short_term_context(channel)
    recent_logs = "\n".join(full_logs.splitlines()[-context_line_length:])
    prompt += recent_logs
    prompt += add_long_term_context(channel)
    prompt += settings.bot_description
    prompt += settings.flavor_prompt
    prompt += settings.response_interaction_instructions
    prompt += f"\n\n {speaker} says: {message}"
    
    # Clean up 
    prompt = re.sub(r'\t+', ' ', prompt)
    prompt = re.sub(r' {2,}', ' ', prompt)
    escaped_prompt = prompt.replace("{", "{{").replace("}", "}}")

    logger.info("\n\n\n***Prompt***: \n\n\n%s \n\n\n", escaped_prompt)
    return prompt