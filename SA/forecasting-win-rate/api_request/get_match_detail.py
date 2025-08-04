# match detail information 호출
import requests

def get_match_detail(match_id: str, api_key: str):
    url = f"https://open.api.nexon.com/suddenattack/v1/match-detail?match_id={match_id}"
    headers = {"x-nxopen-api-key": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        participants = [entry["user_name"] for entry in data.get("match_detail", [])]
        return data, participants
    else:
        raise Exception(f"[get_match_detail] {response.status_code} - {response.text}")

