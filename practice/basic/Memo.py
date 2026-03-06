#簡易メモ帳

FILE_NAME = "memo.txt"

while True:
    print("\n--- 簡易メモ帳 ---")
    print("1: メモを書く")
    print("2: メモを見る")
    print("3: 終了")

    choice = input("番号を選んでください")

    if choice == "1":
        memo = input("メモを入力してください")
        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(memo + "\n")
        print("保存しました")

    elif choice == "2":
        try:
            with open(FILE_NAME,"r",encoding="utf-8") as f:
                content = f.read()
                print("\n--- メモ帳 ---")
                print(content)
        except FileNotFoundError:
            print("まだメモがありません")
            raise
    
    elif choice == "3":
        print("終了します")
        break

    else:
        print("1~3を選んでください")