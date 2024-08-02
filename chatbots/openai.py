from typing import List

from dotenv import load_dotenv
from openai import OpenAI

from .prompt import default_chatbot_prompt

# Load environment variables from a .env file
load_dotenv()


def call_openai(query: List) -> str:
    client = OpenAI()

    messages = [
        {"role": "system", "content": default_chatbot_prompt},
    ] + query

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    res: str = completion.choices[0].message.content
    return res
