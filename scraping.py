from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import os

# スクレイピング部分
url = 'https://tenki.jp/indexes/sleep/5/25/5040/22130/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
data_elements = soup.find_all('p', class_='indexes-telop-0')

def convert_text_to_value(text):
    mapping = {'暖房は必須！': 1, '夜も朝も暖房': 2, '寝る前に暖房': 3, '翌朝少し寒い': 4, 'よく眠れそう': 5}
    return mapping.get(text, 0)

converted_data = [convert_text_to_value(element.get_text(strip=True)) for element in data_elements]

# データベース部分
db_path = '/Users/kageyamayuu/univ./課題/DSpro/sleep_data.sqlite'  # データベースファイルのパス
conn = sqlite3.connect(db_path)
conn.execute('CREATE TABLE IF NOT EXISTS sleep_index (id INTEGER PRIMARY KEY, index_value INTEGER);')
cursor = conn.cursor()
for value in converted_data:
    cursor.execute('INSERT INTO sleep_index (index_value) VALUES (?);', (value,))
conn.commit()
conn.close()

# CSVファイルへの保存部分
csv_path = '/Users/kageyamayuu/univ./課題/DSpro/sleep_data.csv'  # CSVファイルのパス
data_frame = pd.DataFrame({'睡眠指数': converted_data})
data_frame.to_csv(csv_path, index=False)
