#requests　URL内のデータを拾う外部ライブラリ
import requests

url = "https://api.github.com"

response = requests.get(url)

print("ステータス:", response.status_code)
print("内容:")
print(response.text)