from crawler.nickname_crawler import get_top_nicknames
from api_request.char_info import get_ocid
import pandas as pd

if __name__ == "__main__":
    names = get_top_nicknames(100)
    df = pd.DataFrame(names, columns=["nickname"])
    print(f"{len(names)}'s collect complete")
    print(df.head())

    df.to_csv("./nicknames.csv", index=False, encoding="utf-8-sig")