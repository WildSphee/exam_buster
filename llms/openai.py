from typing import Dict, List

from dotenv import load_dotenv
from openai import OpenAI
from telegram import User

# Load environment variables from a .env file
load_dotenv()


def call_openai(
    history: List[Dict[str, str]], user: User, query: str, prompt: str
) -> str:
    client = OpenAI()

    messages = history + [
        {
            "role": "system",
            "content": prompt.format(
                username=user.first_name or "<not provided>", query=query
            ),
        },
    ]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    res: str = completion.choices[0].message.content
    return res
