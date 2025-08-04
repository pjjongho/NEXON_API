# rank infomation 호출
import requests

def get_rank(ouid:str, api_key:str) -> dict:
    url = f"https://open.api.nexon.com/suddenattack/v1/user/rank?ouid={ouid}"
    headesr = {"x-nxopen-api-key":api_key}

    response = requests.get(url, headers=headesr)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"[get_rank] {response.status_code} - {response.text}")