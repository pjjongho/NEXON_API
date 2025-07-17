import time

import requests
from bs4 import BeautifulSoup

def get_top_nicknames(n=500):
    nicknames = []
    page = 1

    while len(nicknames) < n:
        print(f"Crawling .. \n Page : {page}p ({len(nicknames)}/{n})")
        url = f"https://maple.gg/ranks/power?page={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        # 닉네임 추출
        a_tags = soup.find_all("a", href=True)
        name_candidates = [a['href'].split("/u/")[1] for a in a_tags if a['href'].startswith("/u/")]

        if not name_candidates :
            print("Not anymore nicknames")
            break

        for name in name_candidates:
            if name not in nicknames:
                nicknames.append(name)
            if len(nicknames) >= n:
                break

        page +=1 
        time.sleep(0.25)
    return nicknames