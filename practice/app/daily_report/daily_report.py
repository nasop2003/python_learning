from datetime import date
from datetime import datetime
from pathlib import Path
import glob
import os

FILE_PATH = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\practice\app\daily_report\daily_report_file"
TXT_FILE = Path(FILE_PATH) / f"{date.today()}.txt"

def write_txt(text : str) -> None:
    """メモ書き込み"""
    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def new_txt() -> None:
    """新規メモ作成"""

    #今日やったこと（空白だとエラー。最低限メモに必要）
    while True:
        today_report = input("1 今日やったこと: ").strip()
        if today_report == "":
            print("今日やったことは最低でも入力してください")
            continue
        else:
            new_today_report = f"今日やったこと: {today_report}"
            break
    
    #学んだこと（空白でもOK。空白の場合は "なし" と記入）
    learning_report = input("2 学んだこと: ").strip()
    if learning_report == "":
        new_learning_report = f"学んだこと: なし"
    else:
        new_learning_report = f"学んだこと: {learning_report}"
    
    #明日やること（空白でもOK。空白の場合は "なし" と記入）
    tomorrow_report = input("3 明日やること: ").strip()
    if tomorrow_report == "":
        new_tomorrow_report = f"明日やること: なし"
    else:
        new_tomorrow_report = f"明日やること: {tomorrow_report}"
    
    today = datetime.now().strftime("%Y/%m/%d %H:%M")
    
    p = TXT_FILE
    
    while True:
        if p.exists():
            choice = input("すでに同日のテキストファイルがあります。上書きしますか？ y/n ")
            if choice == "y":
                #txtファイルの中身を消去
                with open(p, "w") as f:
                    pass
                
                write_txt(today)
                write_txt(new_today_report)
                write_txt(new_learning_report)
                write_txt(new_tomorrow_report)
                print("上書きしました")
                return
            elif choice == "n":
                print("キャンセルしました")
                return
            else:
                print("yかn のいずれかを入力してください")
                continue
        else:
            write_txt(today)
            write_txt(new_today_report)
            write_txt(new_learning_report)
            write_txt(new_tomorrow_report)
            print("保存しました")
            break
            
def txt_delete() -> None:
    """メモ削除"""
    p = TXT_FILE
    
    if not p.exists():
        print("日報が存在しません")
        return
    
    print("\n---メモ編集---")
    files = glob.glob(f"{FILE_PATH}/*.txt")
    
    for i, f in enumerate(files, start=1):
        print(f"{i} / {os.path.basename(f)}")
    
    while True:
        try:
            choice = int(input("\n削除したいtxtファイルを番号で選択してください: "))
        except ValueError:
            print("番号を入力してください")
            continue
        
        #1が番号の最初になるように調整（-1を代入）
        remove_num = choice - 1
        
        os.remove(files[remove_num])
        print("削除しました")
        break

def main() -> None:
    """メイン画面"""
    while True:
        print("\n---日報ジェネレーター---")
        print("\n1) 日報を書く")
        print("2) 日報削除")
        print("3) 終了")
        
        choice = input("選択: ")
        
        if choice == "1":
            new_txt()
        elif choice == "2":
            txt_delete()
        elif choice == "3":
            print("終了します")
            break
        else:
            print("1~3のいずれかを入力してください")
            continue
    
if __name__ == "__main__":
    main()