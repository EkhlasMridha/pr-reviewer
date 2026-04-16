import os
from openai import OpenAI

def get_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

def call_llm(messages, temperature=0.2):
    client = get_client()
    model = os.getenv("MODEL_NAME", "grok-2-latest")

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content