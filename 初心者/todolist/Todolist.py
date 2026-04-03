import os
import json
from pathlib import Path
from datetime import datetime

def list_add(file_path: str = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\Todoリスト\TodoList.json" ) :
    """Todoリスト追加（文字のみ、数字と記号は入力不可）"""

    path = Path(file_path)
    if path.exists():
        with open(file_path, "r", encoding= "utf-8") as f:
            tasks = json.load(f)
    else:
        tasks = []

    while True:
    
        #空文字（スペース含む）、数字、記号の入力ごとにに表示するメッセージを変える
        todo_list = input("タスク名: ").strip()

        if todo_list == "": 
            print("文字を入力してください")
            continue
        elif todo_list.isdigit(): #数字が入力されていたら最初から入力
            print("数字は入力できません")
            continue
        elif not todo_list.isalpha(): #記号が入力されていたら最初から入力
            print("記号は入力できません")
            continue
        else:
            break
    
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")  #例：2026-03-10 16:30

    tasks.append({"タスク名": todo_list, "日付": date_now})

    with open(file_path, "w", encoding= "utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

    print(f"追加しました。タスク名: {todo_list}, 日付: {date_now}")


def list_show(file_path: str = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\Todoリスト\TodoList.json" ):
    """追加したToDoリストをすべて表示"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding= "utf-8")as f:
            tasks = json.load(f)
        if not tasks:
            print("ToDoリストが空です")
            return
        else:
            print("=" * 18)
            print("登録済のToDoリスト")
            print("=" * 18)

            for i, item in enumerate(tasks, start=1): 
                print(f"{i}. {item['タスク名']} ({item['日付']})") #インデックス番号・タスク名・追加日時が表示される
    else: 
        print("TodoList.jsonが存在しません。")
        return
    


def list_delete(file_path: str = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\Todoリスト\TodoList.json" ):
    """ToDoリスト削除（インデックス番号を選択して削除）"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding= "utf-8")as f:
            tasks = json.load(f)
        
        for i, item in enumerate(tasks, start=1):
            print(f"\n{i}. {item['タスク名']} ({item['日付']})")

        if not tasks:
            print("ToDoリストが空です")
            return
        else:
            try:
                select = int(input("\n削除したいインデックス番号を選択してください"))
            except ValueError:
                print("数字を入力してください")

            tasks.pop(select - 1)

            with open(file_path, "w", encoding= "utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent = 2)

            print("削除しました")
    else:
        print("TodoList.jsonが存在しません")
        return


def main():
    while True:
        print("=" * 10)
        print("ToDoリスト")
        print("=" * 10)

        print("1) 追加")
        print("2) 表示")
        print("3) 削除")
        print("4) 終了")

        choice = input("選択: ")

        if choice == "1":
            list_add()
        elif choice == "2":
            list_show()
        elif choice == "3":
            list_delete()
        elif choice == "4":
            print("終了します")
            return
        else:
            print("1~3のいずれかを入力してください")
            continue

if __name__ == "__main__":
    main()