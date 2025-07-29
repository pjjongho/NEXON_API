from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd
from tqdm import tqdm

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

path = "chromedriver.exe 가 있는 경로 입력"
service = Service(executable_path=path)

driver = webdriver.Chrome(service=service, options=options)

nicknames = []

# 서든은 랭커 페이지에 10명이 등록되어있음
# 100페이지 까지 크롤링해서 총 1천명 수집
for page in tqdm(range(1, 101)):
    url = f"https://sa.nexon.com/ranking/total/ranklist.aspx?n4PageNo={page}&delay=true"
    driver.get(url)
    time.sleep(2.5)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.left a[onclick^='GetUserInfo'] b"))
        )
        nickname_tags = driver.find_elements(By.CSS_SELECTOR, "td.left a[onclick^='GetUserInfo'] b")
        for tag in nickname_tags:
            nickname = tag.text.strip()
            if nickname:
                nicknames.append(nickname)
    except:
        print(f"[경고] {page}페이지 로딩 실패ㅠ")

driver.quit()

df = pd.DataFrame(nicknames, columns=['nickname'])
df.to_csv('./crwaler/nickname.csv', index=False, encoding='utf-8-sig')
