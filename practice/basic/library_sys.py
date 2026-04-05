import sys

value = input("数字を入力してください")

if not value.isdigit():
    print("数字ではないので終了します")
    sys.exit()

print("入力された数字:", value)