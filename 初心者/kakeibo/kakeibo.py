import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import date
from pathlib import Path
import json
import csv
#ウィンドウのレイアウト
#日付　0000-00-00 （１行目）
#種別　　支出・収入 （２行目）
#カテゴリ　プルダウン（３行目）
#金額   入力フォーム（４行目）
#メモ   入力フォーム（５行目）
#登録ボタン（６行目）
#家計簿一覧の切り替えボタン（７行目）
#家計簿一覧（右に収入・支出・収支の合計を表示）（８行目）
def load_categories(file_path: str = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\kakeibo\category.json"):
    """json読み込み、無ければ作成（支出・収入カテゴリ）"""
    path = Path(file_path)
    if path.exists():
        with open(file_path, "r", encoding= "utf-8") as f:
            categories = json.load(f)
    else:
        categories = {
            "支出": [],
            "収入": []
        }

        categories["支出"].extend(["食費", "交通費", "光熱費", "娯楽", "その他"]) #初期カテゴリ「食費」「交通費」「光熱費」「娯楽」「その他」
        categories["収入"].extend(["給与", "副収入", "その他"])                  #初期カテゴリ「給与」「副収入」「その他」

        with open(file_path, "w", encoding= "utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)
    return categories

def load_csv(data_csv: str = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\kakeibo\kakeibo.csv"):
    """csv書き込み（無ければ作成）。家計簿の書き込みはこのcsvファイルを使う"""
    path = Path(data_csv)
    if path.exists():
        with open(data_csv, "r", encoding="utf-8") as f:
            csv.reader(f)
    else:
        with open(data_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "type", "category", "amount", "memo"])
    return path, data_csv

def build_form(root, refresh):
    """入力フォーム（日付・種別・カテゴリ・金額・メモ・登録）"""
    #日付（カレンダーで選択できるように設置）
    date_var = tk.StringVar(value=str(date.today()))

    def open_calender():
        """カレンダー作成（別ウィンドウで表示）"""
        popup = tk.Toplevel(root)
        popup.title("日付選択")

        cal = Calendar(
            popup, date_pattern="yyyy-mm-dd",
            locale="ja_JP",
            firstweekday="sunday",
            showweeknumbers=False,
            showothermonthdays=False,
            selectmode="day"
        )
        cal.pack()

        def on_date_select(event):
            date_var.set(cal.get_date())
            popup.after(1, popup.destroy)

        cal.bind("<<CalendarSelected>>", on_date_select)

    #日付ボタン（１行目）
    tk.Label(root, text="日付").grid(row=0, column=0)
    tk.Button(root, textvariable=date_var, command=(open_calender),relief="groove").grid(row=0, column=1)

    #種別（タイトルと右に支出・収入タブ（切り替え）を配置。）（２行目）
    tk.Label(root, text="種別").grid(row=1, column=0)

    var = tk.StringVar(value="支出") #初期値

    type_frame = tk.Frame(root)
    type_frame.grid(row=1, column=1)

    tk.Radiobutton(type_frame, text="支出", variable=var, value="支出").grid(row=0, column=0, padx=4)
    tk.Radiobutton(type_frame, text="収入", variable=var, value="収入").grid(row=0, column=1, padx=4)

    #カテゴリ（種別に連動したドロップダウンを作成）（３行目）
    categories = load_categories()

    tk.Label(root, text="カテゴリ").grid(row=2, column=0)
    combo = ttk.Combobox(root, state= "readonly") #←先に定義
    combo.grid(row=2, column=1)

    def update_categories(*args):
        combo["values"] = categories[var.get()]
        combo.set(categories[var.get()][0])

    var.trace_add("write", update_categories)
    update_categories()

    #金額（数字を入力）（４行目）
    amount_label =tk.Label(root, text="金額")
    amount_label.grid(row=3, column=0)

    #入力フォーム
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=3, column=1)

    #メモ（文字列）（５行目）
    memo_label = tk.Label(root, text="メモ")
    memo_label.grid(row=4, column=0)

    #入力フォーム
    memo_entry = tk.Entry(root)
    memo_entry.grid(row=4, column=1)
    
    #登録（入力情報すべてを登録。金額部分が数字以外で入力されていればエラーを出す）
    def register(data_csv: str = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\kakeibo\kakeibo.csv"):
        """登録（日付・種別・カテゴリ・金額・メモ）メモは空白でもOK、金額は数字のみ登録できるように設計。登録したら家計簿一覧画面を更新"""
        date = date_var.get()
        type = var.get()
        category = combo.get()
        amount = amount_entry.get().strip()
        memo = memo_entry.get()

        if amount == "":
            messagebox.showerror("金額入力エラー", "数字を入力してください")
            return
        elif amount.isalpha(): #文字列チェック
            messagebox.showerror("金額入力エラー", "文字列は入力できません")
            return
        elif not amount.isdigit(): #記号チェック（記号・混合）
            messagebox.showerror("金額入力エラー", "記号は入力できません")
            return
        else:
            with open(data_csv, "a", newline="", encoding= "utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([date, type, category, amount, memo])
            refresh()

        messagebox.showinfo("登録完了", "登録しました。")

    #登録ボタン（６行目）
    register_button = tk.Button(root, text = "登録", command= register)
    register_button.grid(row=5, column=1)

def build_sumary(root, data_csv: str = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\kakeibo\kakeibo.csv"):
    """支出・収入合計、家計簿一覧を表示"""
    income = 0 #収入合計
    expence = 0 #支出合計

    with open(data_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            type = row[1]
            amount = int(row[3])
        
            if type == "収入":
                income += amount
            elif type == "支出":
                expence += amount
    
    total_frame = tk.Frame(root)
    total_frame.grid(row=7, column=2)

    tk.Label(total_frame, text=f"収入合計: {int(income):,}円").grid(row=0, column=0, padx=2)
    tk.Label(total_frame, text=f"支出合計: {int(expence):,}円").grid(row=1, column=0, padx=2)
    tk.Label(total_frame, text=f"収支合計: {int(income - expence):,}円").grid(row=2, column=0, padx=2)

    #家計簿一覧を表示（８行目）
    frame = tk.Frame(root)
    frame.grid(row=7, column=1)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.grid(row=6, column=4)
    
    text = tk.Text(frame, yscrollcommand=scrollbar.set, width=40, height=10)
    text.grid(row=6, column=1)

    scrollbar.config(command=text.yview)

    var = tk.StringVar(value="すべて") 

    def refresh():
        text.config(state=tk.NORMAL)
        text.delete("1.0", tk.END)
        with open(data_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if var.get() ==  "すべて" or row[1] == var.get():   
                    text.insert(tk.END, f"{row[0]} {row[1]} {row[2]} {int(row[3]):,}円 {row[4]}\n")
        text.config(state=tk.DISABLED) #編集不可に戻す

    #家計簿一覧
    filter_frame = tk.Frame(root)
    filter_frame.grid(row=6, column=1)

    tk.Radiobutton(filter_frame, text="すべて", variable=var, value="すべて", command=refresh).grid(row=1, column=1, padx=4)
    tk.Radiobutton(filter_frame, text="支出", variable=var, value="支出", command=refresh).grid(row=1, column=1, padx=4)
    tk.Radiobutton(filter_frame, text="収入", variable=var, value="収入", command=refresh).grid(row=1, column=2, padx=4)

    refresh()
    return refresh

def main_window():
    root = tk.Tk()
    root.title("簡易家計簿")
    root.geometry("500x400") #　幅x高さ
    load_categories()
    load_csv()
    refresh = build_sumary(root)
    build_form(root, refresh)
    root.mainloop()

if __name__ == "__main__":
    main_window()