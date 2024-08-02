import requests
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

# Load environment variables from a .env file
load_dotenv()


def call_openai(prompt: str):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"{prompt}"},
        ],
    )

    print(completion.choices[0].message)


# Example usage
if __name__ == "__main__":
    prompt = "Tell me a joke about cats."

    try:
        call_openai(prompt=prompt)
    except ValidationError as e:
        print("Validation error:", e.json())
    except requests.RequestException as e:
        print("Request error:", str(e))
