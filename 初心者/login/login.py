#ログイン認証システム
import sys

def login_register():
    """ユーザー情報登録"""

    username = input("ユーザー名を登録: ")
    password = input("パスワードを登録: ")

    user1 = {username: password}
    print("登録しました")
    return user1

def login(user_data):
    """ログイン情報を入力。３回間違えたら終了"""

    attempt = 0

    while attempt < 3:
        username = input("ユーザー名: ")
        password = input("パスワード: ")

        login_data = {username: password}

        if user_data == login_data:
            print("ログインしました")
            break
        else:
            attempt += 1
            print(f"ログインに失敗しました。残り回数: {3 - attempt}")

    if attempt == 3:   
        print("試行回数が上限を達しました。もう一度やり直してください。")
        sys.exit()

def main():
    user_data = None

    while True:
        print("=" * 20)
        print("ログイン認証システム")
        print("=" * 20)
        print("1) ユーザー情報入力")
        print("2) ログイン")
        print("3) 終了")

        choice = input("選択: ")

        if choice == "1":
            user_data = login_register()
        elif choice == "2":
            if user_data is None:
                print("ユーザー情報が登録されていません。")
                continue
            login(user_data)
        elif choice == "3":
            print("終了します")
            break
        else:
            print("1~3をいずれかを選択してください")

if __name__ == "__main__":
    main()


        


