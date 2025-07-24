import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # 서버 이름과 maskGameCode 매핑
    server_code_map = {
        '연': '131073',
        '무휼': '131074',
        '유리': '131086',
        '하자': '131087',
        '호동': '131088',
        '진': '131089'
    }

    # 직업 이름과 class 이름 매핑
    job_class_map = {
        '전사': 'warrior',
        '도적': 'thief',
        '주술사': 'magician',
        '도사': 'ascetic',
        '궁사': 'archer',
        '천인': 'skyhm',
        '마도사': 'mado',
        '영술사': 'magician2',
        '차사': 'chasa',
        '살수': 'salsu'
    }

    # 크롬 드라이버 설정
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    CHROMEDRIVER_PATH = r"C:\Users\jjong\Desktop\Practice\NEXON_API\Baram\crwaler\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    result = []

    for server_name, server_code in server_code_map.items():
        url = f"https://baram.nexon.com/Rank/List?maskGameCode={server_code}"
        driver.get(url)
        time.sleep(2)

        for job_name, job_class in job_class_map.items():
            try:
                # 직업 탭 클릭
                driver.find_element(By.CLASS_NAME, job_class).click()

                # 닉네임 로딩 기다림
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.gameid > a"))
                )

                nickname_tags = driver.find_elements(By.CSS_SELECTOR, "td.gameid > a")

                for rank, tag in enumerate(nickname_tags[:10], 1):  # 상위 10명만 총 600명
                    nickname = tag.text.strip()
                    result.append({
                        "게임아이디": nickname,
                        "서버": server_name,
                        "직업": job_name,
                        "순위": rank
                    })

            except Exception as e:
                print(f"[ERROR] {server_name} - {job_name}: {e}")
                continue

    driver.quit()

    # 저장
    os.makedirs("./data", exist_ok=True)
    df = pd.DataFrame(result)
    df.to_csv("./Baram/data/baram_ranker.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()
