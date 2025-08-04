# recent information 호출

import requests

def get_recent_info(ouid:str, api_kay:str) -> dict:
    url = f"https://open.api.nexon.com/suddenattack/v1/user/recent-info?ouid={ouid}"
    headers = {"x-nxopen-api-key":api_kay}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"[get_recent_info] {response.status_code} - {response.text}")