# ouid 호출

import requests

def get_ouid(nickname: str, api_key: str) -> str | None:
    url = f"https://open.api.nexon.com/suddenattack/v1/id?user_name={nickname}"
    headers = {"x-nxopen-api-key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["ouid"]
    else:
        print(f"[SKIP] 유저 '{nickname}'는 OUID를 못가져옴 (status {response.status_code})")
        return None


    