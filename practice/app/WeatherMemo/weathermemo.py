import json
from datetime import datetime
from pathlib import Path

FILE_PATH = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\WeatherMemo\weathermemo.json"

def load_json() -> list[dict]:
    """jsonファイル読み込み"""
    path = Path(FILE_PATH)
    if path.exists():
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            weather_memo = json.load(f)
    else:
        weather_memo = []
        save_json(weather_memo)
    return weather_memo

def save_json(weather_memo: list[dict]) -> None:
    """jsonファイル保存"""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(weather_memo, f, ensure_ascii=False, indent=2)

def input_memo(weather_memo: list[dict]) -> None:
    """メモ入力"""
    #今日の気温を入力（小数入力可、それ以外はエラー）

    today = datetime.now().strftime("%Y/%m/%d")

    while True:

        try:
            temperature = float(input("今日の気温： ").strip())
        except ValueError: #文字を入力したらエラー（小数は入力可能にする）
            print("数字（小数入力可）を入力してください")
            continue

        temperature_memo = {"気温": temperature}
        break
    
    #今日の天気を入力（選択式）
    while True:
        print("今日の天気")
        print("1) 晴れ")
        print("2) くもり")
        print("3) 雨")
        print("4) 雪")

        choice = input("今日の天気を選択: ")
        if choice == "1":
            weather = {"天気": "晴れ"}
            break
        elif choice == "2":
            weather ={"天気": "くもり"}
            break
        elif choice == "3":
            weather = {"天気": "雨"}
            break
        elif choice == "4":
            weather = {"天気": "雪"}
            break
        else:
            print("1~4のいずれかを選択してください")
            continue

    #メモを入力（自由記述）
    text = input("メモを入力:").strip()
        
    text_memo = {"メモ": text}
    today_memo = {"日付": today}

    memos = {
        **today_memo,
        **temperature_memo,
        **weather,
        **text_memo,
    }

    #同日のメモが存在するか確認。なければ追加
    for m in weather_memo:
        if m['日付'] == today:
            print("同日のメモが存在するため、追加できません")
            return
    else:
        print("追加しました")
        weather_memo.append(memos)
        save_json(weather_memo)
        return

def memo_list(memos: list[dict]) -> None:
    """メモ一覧表示"""   
    print("=" * 8)
    print("メモ一覧")
    print("=" * 8)

    for m in memos:
        print(f" {m['日付']} / {m['気温']} / {m['天気']} / {m['メモ']}")

def main() -> None:
    """メイン画面"""

    while True:
        print("=" * 10)
        print("天気メモ帳")
        print("=" * 10)

        print("\n1) メモ作成")
        print("2) メモ一覧")
        print("3) 終了")

        choice = input("選択: ")

        if choice == "1":
            weather_memo = load_json()
            input_memo(weather_memo)
        elif choice == "2":
            memos = load_json()
            memo_list(memos)
        elif choice == "3":
            print("終了します")
            return
        else:
            print("1~3のいずれかを選択してください")
            continue

if __name__ == "__main__":
    load_json()
    main()