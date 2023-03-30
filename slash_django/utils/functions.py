import os
import openai
import requests
from dotenv import load_dotenv

dotenv_path = '/home/kommonio/slash-django/Slash/.env'
load_dotenv(dotenv_path)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PARAPHRASE_API_KEY = os.getenv("PARAPHRASE_API_KEY")
PARAPHRASE_API_URL = os.getenv("PARAPHRASE_API_URL")

openai.api_key = OPENAI_API_KEY

def call_chat_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message

def call_paraphrase_api(prompt):
    headers = {
        "x-api-key": PARAPHRASE_API_KEY,
    }
    data = {
        "text": prompt
    }
    response = requests.post(PARAPHRASE_API_URL, headers=headers, json=data)
    response_text = response.json()["text"]
    return response_text

def call_dalle(prompt):
    # Replace with the necessary code to call the DALL-E API
    pass

def process_prompt(prompt, chosen_model):
    if chosen_model == "Write":
        return call_chat_gpt(prompt)
    elif chosen_model == "Paraphrase":
        return call_paraphrase_api(prompt)
    elif chosen_model == "Imagine":
        return call_dalle(prompt)
    else:
        return "Invalid model chosen."
