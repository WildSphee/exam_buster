from dotenv import load_dotenv
from openai import OpenAI

from .prompt import default_chatbot_prompt

# Load environment variables from a .env file
load_dotenv()


def call_openai(query: str) -> str:
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": default_chatbot_prompt},
            {"role": "user", "content": query},
        ],
    )

    res: str = completion.choices[0].message.content
    return res
