# basic 정보 호출

import requests

def get_basic(ouid : str, api_key:str) -> dict:
    url = f"https://open.api.nexon.com/suddenattack/v1/user/basic?ouid={ouid}"
    headers = {"x-nxopen-api-key":api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"[get_basic] {response.status_code} - {response.text}")