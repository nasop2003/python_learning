import json
import random
from pathlib import Path

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
        
def vocabulary_register():
    """単語登録"""

def vocabulary_list():
    """単語一覧表示"""

def test_questions():
    """テスト問題出題（１問）"""
    
def answer_check():
    """正誤判定"""

def summary_results():
    """集計・結果表示"""
    
def main():
    """メイン画面"""

if __name__ == "__main__":
    main()