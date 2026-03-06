import os

print("現在のフォルダ:", os.getcwd())
print("フォルダ内のファイル一覧:")

files = os.listdir()

for file in files:
    print(file)