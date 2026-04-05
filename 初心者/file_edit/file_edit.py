#ファイルに書き込む
text = input("保存したい文字を入力してください: ")

with open("File.txt", "a", encoding="utf-8") as file:
    file.write(text + "\n")

print("保存しました")

#ファイルを書き込む
with open("File.txt", "r", encoding="utf-8") as file:
    content = file.read()

print("ファイルの中身は: ")
print(content)