# match information 호출
import requests
from urllib.parse import quote

def get_match(ouid: str, api_key: str, mode: str = "폭파미션", mtype: str = "퀵매치 클랜전") -> list:
    mode_encoded = quote(mode)
    mtype_encoded = quote(mtype)

    url = f"https://open.api.nexon.com/suddenattack/v1/match?ouid={ouid}&match_mode={mode_encoded}&match_type={mtype_encoded}"
    headers = {"x-nxopen-api-key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return [match["match_id"] for match in response.json().get("match", [])]
    else:
        raise Exception(f"[get_match_list] {response.status_code} - {response.text}")

