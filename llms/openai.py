from typing import Dict, List

from dotenv import load_dotenv
from openai import OpenAI
from telegram import User

from .prompt import default_chatbot_prompt

# Load environment variables from a .env file
load_dotenv()


def call_openai(
    query: List[Dict[str, str]], user: User, prompt: str = default_chatbot_prompt
) -> str:
    client = OpenAI()

    messages = [
        {
            "role": "system",
            "content": prompt.format(username=user.first_name or "<not provided>"),
        },
    ] + query

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    res: str = completion.choices[0].message.content
    return res
