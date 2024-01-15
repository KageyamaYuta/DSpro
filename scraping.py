from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import os

# スクレイピング部分（既存のコード）
url = 'https://tenki.jp/indexes/sleep/5/25/5040/22130/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
data_elements = soup.find_all('p', class_='indexes-telop-0')

def convert_text_to_value(text):
    mapping = {'暖房は必須！': 1, '夜も朝も暖房': 2, '寝る前に暖房': 3, '翌朝少し寒い': 4, 'よく眠れそう': 5}
    return mapping.get(text, 0)

converted_data = [convert_text_to_value(element.get_text(strip=True)) for element in data_elements]

# データベースへの保存部分
db_path = '/Users/kageyamayuu/univ./課題/DSpro/sleep_data.db'  # データベースファイルのパス

# データベースに接続（なければ新規作成）
conn = sqlite3.connect(db_path)

# データベースにテーブルを作成（すでに存在する場合はスキップ）
conn.execute('CREATE TABLE IF NOT EXISTS sleep_index (id INTEGER PRIMARY KEY, index_value INTEGER);')

# データをデータベースに挿入
cursor = conn.cursor()
for value in converted_data:
    cursor.execute('INSERT INTO sleep_index (index_value) VALUES (?);', (value,))

# 変更をコミットして接続を閉じる
conn.commit()
conn.close()
