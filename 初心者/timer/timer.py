import time
from datetime import datetime
import json
from pathlib import Path

def timer(seconds: int) -> int:
    """指定した秒数を0になるまでカウントダウンする"""

    for i in range(seconds, 0, -1):
        print(f"残り: {i}秒")
        time.sleep(1)
    print("終了")
    while True:
        choice = input("記録内容を保存しますか？ y/n ")

        if choice == "y":
            save_history(seconds)
            break
        elif choice == "n":
            return
        else:
            print(" y か n のいずれかを入力してください")
            continue

def select_time() -> int:
    """秒数を指定する"""
    while True:
        try:
            seconds = int(input("秒数: "))
        except ValueError:
            print("数字を入力してください")
            continue
        if seconds == 0:
            print("0秒は入力できません")
            continue
        return seconds

def save_history(seconds:int, file_path: str = "timer_history.json" ) -> None: #保存先はフォルダ「Python」保存するjson名は「timer_history.json」
    """結果内容を記録する"""
    data = {
        "実行日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "秒数": seconds
    }

    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():        
        with open(file_path, "r", encoding= "utf-8") as f:
            history = json.load(f)
    else:
        history = []
    
    history.append(data)

    with open("timer_history.json", "w", encoding= "utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)
    
    print("記録しました")
    return data

def show_history(file_path: str = "timer_history.json") -> None: 
    """記録内容を表示"""
    path = Path(file_path)

    if not path.exists():
        print("記録内容がありません")
        return
    
    with open(path, "r", encoding="utf-8") as f:
        history = json.load(f)

    for item in history:
        print("=" * 30)
        print(f"実行日時: {item['実行日時']}")
        print(f"秒数: {item['秒数']}")
        print("=" * 30)



def main():
    while True:
        print("=" * 15)
        print("簡易タイマー")
        print("=" * 15)
        print("1) 実行")
        print("2) 記録内容表示")
        print("3) 終了")

        choice = input("選択: ")
        if choice == "1":
            seconds = select_time()
            timer(seconds)
        elif choice == "2":
            show_history()
        elif choice == "3":
            print("終了します")
            break

if __name__ == "__main__":
    main()