import json
import random
from pathlib import Path
from datetime import datetime
import re

FILE_PATH = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\practice\app\word_list\word_list.json"

def json_load() -> dict[list]:
    """jsonファイル読み込み"""
    path = Path(FILE_PATH)
    if path.exists():
        with open(FILE_PATH, "r", encoding= "utf-8") as f:
            data = json.load(f)
    else:
        data = {"単語": [], "テスト結果": []}
        json_save(data)
    return data

def json_save(data: dict[list]) -> None:
    """json保存"""
    with open(FILE_PATH, "w", encoding= "utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def word_check(data: dict[list]) -> bool:
    """jsonファイル内の単語が存在するか確認"""
    if not data["単語"]:
        print("単語が登録されていません")
        return True
    else:
        return False

def is_japanese(text: str) -> bool:
    """日本語判定"""
    pattern = re.compile(r'[\u3041-\u3096\u30A0-\u30FF\u4E00-\u9FFF]')
    return bool(pattern.search(text))

def word_register(word: dict[list]) -> None:
    """単語登録"""
    
    #英単語を登録（数字・記号・日本語は入力不可）
    while True:
        
        english_word = input("英単語を入力: ").strip()
        
        if english_word == "":
            print("文字を入力してください")
            continue
        elif english_word.isdigit():
            print("数字は入力できません")
            continue
        elif not english_word.isalpha():
            print("記号は入力できません")
            continue
        elif is_japanese(english_word):
            print("日本語は入力できません")
        else:
            break
    
    #日本語訳を登録（数字・記号・英語は入力不可）
    while True:
        japanese_word = input("日本語訳を入力: ").strip()
        
        if japanese_word == "":
            print("文字を入力してください")
            continue
        elif japanese_word.isdigit():
            print("数字は入力できません")
            continue
        elif not japanese_word.isalpha():
            print("記号は入力できません")
            continue
        elif japanese_word.isalpha() and japanese_word.isascii():
            print("英語は入力できません")
            continue
        else:
            #英単語・日本語訳すべてクリアしたときの処理
            new_word = {"英単語": english_word, "訳": japanese_word}
            word["単語"].append(new_word)
            
        json_save(word)
        print(f"登録しました。英単語: {english_word} ・ 日本語訳: {japanese_word}")
        break

def word_list(data: dict[list]):
    """単語一覧表示"""
    print("英単語一覧")
    
    for i, v in enumerate(data["単語"], start=1):
        print(f"{i} / {v['英単語']} / {v['訳']}")
        
def test_questions(data: dict[list]) -> str:
    """テスト問題出題（１問）"""
    print("=" *4)
    print("問題")
    print("=" *4)
    
    d = data["単語"]
    
    problem = random.choice(d[0]["英単語"])
    answer = input(f"{problem}の日本語は？: ")
    return answer_check(data, answer)

def answer_check(data: dict[list], answer: str):
    """正誤判定"""
    d = data["単語"]
    
    if answer == d[0]["訳"]:
        print("〇")
    else:
        print("×")

def summary_results(data: dict[list]):
    """集計・結果表示"""

def main() -> None:
    """メイン画面"""
    print("=" * 6)
    print("単語帳")
    print("=" * 6)
    
    while True:
        data = json_load()
        
        print("\n1) 単語登録")
        print("2) 単語一覧表示")
        print("3) テスト")
        print("4) 集計・結果表示")
        print("5) 終了")
        
        choice = input("メイン画面・選択: ")
        
        if choice == "1":
            word_register(data)
        elif choice == "2":
            if word_check(data):
                continue
            else:
                word_list(data)
        elif choice == "3":
            if word_check(data):
                continue
            else:
                test_questions(data)
        elif choice == "4":
            if word_check(data):
                continue
            else:
                summary_results(data)
        elif choice == "5":
            print("終了します")
            break
        else:
            print("1~5のいずれかを入力してください")
            continue
            
if __name__ == "__main__":
    main()