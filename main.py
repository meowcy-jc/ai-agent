import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)




def ask_question(user_prompt: str):
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    )

    if "--verbose" in sys.argv:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    print(response.text)


def get_answer():
    if len(sys.argv) < 2:
        print("Usage: uv ran main.py <question>")
        sys.exit(1)
    else:
        ask_question(sys.argv[1])

get_answer()

