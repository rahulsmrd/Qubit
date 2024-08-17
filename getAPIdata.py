import os
import requests

from dotenv import load_dotenv

load_dotenv()

def get_data_from_api(payload):
    try:
        url = os.getenv('RAPID_API_URL')
        headers = {
        'x-rapidapi-key': os.getenv("RAPID_API_KEY"),
        'x-rapidapi-host': os.getenv("RAPID_API_HOST"),
        'Content-Type': "application/json",
        'x-rapidapi-user': os.getenv("RAPID_API_USER"),
        }
        data = requests.post(url, json=payload, headers=headers)
        return data.json()
    except Exception as e:
        print(f"ERROR in api : {e}")