# tier information 호출
import requests

def get_tier(ouid:str, api_key:str) -> dict:
    url = f"https://open.api.nexon.com/suddenattack/v1/user/tier?ouid={ouid}"
    headers = {"x-nxopen-api-key":api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"[get_tier] {response.status_code} - {response.text}")