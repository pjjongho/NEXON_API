# Baram/api_request/id/char_id.py

import os
import requests
from urllib.parse import quote

# API 키 불러오기
filename = './baram_1.txt'
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, filename)

with open(filepath, 'r') as file:
    api_key = file.read().strip()

headers = {"x-nxopen-api-key": api_key}

# ID 조회 함수
def get_id(character_name, server_name):
    try:
        encoded_name = quote(character_name)
        encoded_server = quote(server_name)
        url = f"https://open.api.nexon.com/baram/v1/id?character_name={encoded_name}&server_name={encoded_server}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json().get("ocid")
        else:
            print(f'[ERROR] FAILED ID - {character_name} ({server_name}) : {response.status_code} {response.text}')
            return None
    except Exception as e:
        print(f'[EXCEPTION] {character_name} ({server_name}) : {e}')
        return None
