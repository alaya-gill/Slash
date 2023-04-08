import os
import openai
import requests
import base64
import uuid
from dotenv import load_dotenv
from django.conf import settings

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
    response = openai.Image.create(
    prompt=prompt,
    model="image-alpha-001",
    size="256x256",
    response_format="b64_json"
    )
    print()
    unique_id = str(uuid.uuid4())
    path = settings.ROOT_FILE_PATH + "slash_django/static/images/dall_e/{}.jpg".format(unique_id)
    with open(path, "wb") as f:
        f.write(base64.b64decode(response["data"][0]['b64_json']))
    return "/static/images/dall_e/"+unique_id+".jpg"

def process_prompt(prompt, chosen_model):
    if chosen_model == "Write":
        return call_chat_gpt(prompt)
    elif chosen_model == "Paraphrase":
        return call_paraphrase_api(prompt)
    elif chosen_model == "Imagine":
        return call_dalle(prompt)
    else:
        return "Invalid model chosen."
