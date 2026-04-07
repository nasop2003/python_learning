import json
import random
from pathlib import Path
import re

FILE_PATH = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\practice\app\vocabulary_list\vocabulary_list.json"

def json_load() -> list[dict]:
    """jsonファイル読み込み"""
    path = Path(FILE_PATH)
    if path.exists():
        with open(FILE_PATH, "r", encoding= "utf-8") as f:
            vocabulary = json.load(f)
    else:
        vocabulary = []
        json_save(vocabulary)
    return vocabulary

def json_save(vocabulary: list[dict]) -> None:
    """json保存"""
    with open(FILE_PATH, "w", encoding= "utf-8") as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)

def vocabulary_check(vocabulary: list[dict]) -> bool:
    """jsonファイル内の単語が存在するか確認"""
    if not vocabulary:
        print("単語が登録されていません")
        return True
    else:
        return False

def is_japanese(text: str) -> bool:
    """日本語判定"""
    pattern = re.compile(r'[\u3041-\u3096\u30A0-\u30FF\u4E00-\u9FFF]')
    return bool(pattern.search(text))

def vocabulary_register(vocabulary: list[dict]) -> None:
    """単語登録"""
    #英単語を登録（数字・記号・日本語は入力不可）
    while True:
        
        english_vocabulary = input("英単語を入力: ").strip()
        
        if english_vocabulary == "":
            print("文字を入力してください")
            continue
        elif english_vocabulary.isdigit():
            print("数字は入力できません")
            continue
        elif not english_vocabulary.isalpha():
            print("記号は入力できません")
            continue
        elif is_japanese(english_vocabulary):
            print("日本語は入力できません")
        else:
            break
    
    #日本語訳を登録（数字・記号・英語は入力不可）
    while True:
        japanese_vocabulary = input("日本語訳を入力: ").strip()
        if japanese_vocabulary == "":
            print("文字を入力してください")
            continue
        elif japanese_vocabulary.isdigit():
            print("数字は入力できません")
            continue
        elif not japanese_vocabulary.isalpha():
            print("記号は入力できません")
            continue
        elif japanese_vocabulary.isalpha() and japanese_vocabulary.isascii():
            print("英語は入力できません")
            continue
        
        if vocabulary:
            vocabulary[0][english_vocabulary] = japanese_vocabulary #既存のdictに追加
        else:
            vocabulary.append({english_vocabulary: japanese_vocabulary}) #初回のみ新規作成
        
        json_save(vocabulary)
        print(f"登録しました。英単語: {english_vocabulary} ・ 日本語訳: {japanese_vocabulary}")
        return

def vocabulary_list():
    """単語一覧表示"""

def test_questions():
    """テスト問題出題（１問）"""
    
def answer_check():
    """正誤判定"""

def summary_results():
    """集計・結果表示"""

def main() -> None:
    """メイン画面"""
    print("=" * 6)
    print("単語帳")
    print("=" * 6)
        
    print("1) 単語登録")
    print("2) 単語一覧表示")
    print("3) テスト")
    print("4) 集計・結果表示")
    print("5) 終了")
    
    while True:
        vocabulary = json_load()
        
        choice = input("メイン画面・選択: ")
        
        if choice == "1":
            vocabulary_register(vocabulary)
        elif choice == "2":
            if vocabulary_check(vocabulary):
                continue
            else:
                vocabulary_list(vocabulary)
        elif choice == "3":
            if vocabulary_check():
                continue
            else:
                test_questions(vocabulary)
        elif choice == "4":
            if vocabulary_check():
                continue
            else:
                summary_results(vocabulary)
        elif choice == "5":
            print("終了します")
            break
        else:
            print("1~5のいずれかを入力してください")
            continue
            
if __name__ == "__main__":
    main()