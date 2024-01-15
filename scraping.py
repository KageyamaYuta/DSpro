from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# 新しいURL
url = 'https://tenki.jp/indexes/sleep/5/25/5040/22130/'

# リクエストを送り、レスポンスを取得
response = requests.get(url)

# BeautifulSoupオブジェクトの作成
soup = BeautifulSoup(response.text, "html.parser")

# スクレイピング対象のデータを抽出
data_elements = soup.find_all('p', class_='indexes-telop-0')

# テキスト抽出と数値変換
def convert_text_to_value(text):
    mapping = {
        '暖房は必須！': 1,
        '夜も朝も暖房': 2,
        '寝る前に暖房': 3,
        '翌朝少し寒い': 4,
        'よく眠れそう': 5
    }
    return mapping.get(text, 0)  # デフォルト値は0

converted_data = [convert_text_to_value(element.get_text(strip=True)) for element in data_elements]

# Pandas DataFrameの作成
data_frame = pd.DataFrame({'睡眠指数': converted_data})

# 新しいディレクトリ
save_dir = '/Users/kageyamayuu/univ./課題/DSpro/'
file_name = 'tenki_data.csv'
file_path = os.path.join(save_dir, file_name)

# CSVファイルに保存
data_frame.to_csv(file_path, index=False)
