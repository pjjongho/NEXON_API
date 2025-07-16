import warnings
warnings.filterwarnings(action='ignore')

import os
import requests
import pandas as pd
from tqdm import tqdm
import time
from urllib.parse import quote

# api 파일 불러오기

filename = 'api_keys.txt'
base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, filename)

with open(filepath, 'r') as file:
    api_key = file.read().strip()

headers = {"x-nxopen-api-key":api_key}

# OCID (character id) search

def get_ocid(character_name):
    url = f"https://open.api.nexon.com/maplestory/v1/id?character_name={character_name}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("ocid")
    else:
        print('failed ocid search',response.status_code, response.text)
        return None
    

# 캐릭터 기본 정보 조회

def get_character_info(ocid):
    url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("캐릭터 정보 조회 실패 : ", response.status_code, response.text)
        return None
    
if __name__ == "__main__":
    char_name = input("Enter user name : ").strip()
    ocid = get_ocid(char_name)

    if ocid:
        info = get_character_info(ocid)
        if info:
            print(f"character name : {info['character_name']}")
            print(f"job : {info['character_class']}")
            print(f"character level : {info['character_level']}")
            print(f"World : {info['world_name']}")
            #print(f"Stat_info : {info['use_preset_no']}")