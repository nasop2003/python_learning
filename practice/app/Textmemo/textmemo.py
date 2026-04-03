import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pathlib import Path

FILE_PATH = r"C:\Users\ahsom\Desktop\プログラミング学習\Python\初心者\textmemo\textmemo.json"

def load_json():
    """jsonファイル読み込み（無ければ作成）"""
    path = Path(FILE_PATH)
    if path.exists():
        with open(FILE_PATH, "r", encoding= "utf-8" ) as f:
            memo = json.load(f)
    else:
        memo = []
        with open(FILE_PATH, "w", encoding= "utf-8") as f:
            json.dump(memo, f, ensure_ascii=False, indent=2)
    return memo

def main():
    """メイン画面。Tkinterで操作する"""
    load_json()
    root = tk.Tk()
    root.title("メモ帳")
    root.geometry("200x150") #幅x高さ

    root.columnconfigure(0, weight=1)

    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0)

    #メモ作成ボタン
    register_window = [None]
    register_button = tk.Button(button_frame, text="メモ作成", command=lambda: register_memo_window(root, register_window))
    register_button.grid(row=0, column=0, pady=10)

    #メモ検索ボタン
    search_window = [None]
    search_button = tk.Button(button_frame, text="メモ検索", command=lambda: search_memo_window(root, search_window))
    search_button.grid(row=1, column=0, pady=10)

    #メモ編集ボタン
    edit_window = [None]
    edit_button = tk.Button(button_frame, text="メモ編集", command= lambda: edit_memo_window(root, edit_window))
    edit_button.grid(row=2, column=0, pady=10)

    root.mainloop()

def register_memo_window(root, register_window):
    """メモ作成ウィンドウ"""
    #ウィンドウが重複して表示されないよう設計
    if register_window[0] is not None and register_window[0].winfo_exists():
        register_window[0].lift()
        return
    else:
        register_window[0] = tk.Toplevel(root)
        register_window[0].title("メモ作成")
        register_window[0].geometry("300x80") #幅x高さ

    #タイトル
    title_label = tk.Label(register_window[0], text="タイトル")
    title_label.grid(row=0, column=0)

    title_entry = tk.Entry(register_window[0], width=30)
    title_entry.grid(row=0, column=1)

    #本文
    text_label = tk.Label(register_window[0], text="内容")
    text_label.grid(row=1, column=0)

    text_entry = tk.Entry(register_window[0], width=30)
    text_entry.grid(row=1, column=1)

    #タグ
    tag_label = tk.Label(register_window[0], text="タグ")
    tag_label.grid(row=2, column=0)

    tag_entry = tk.Entry(register_window[0], width=30)
    tag_entry.grid(row=2, column=1)

    #登録ボタン
    register_button = tk.Button(register_window[0], text="登録", command=lambda: register_memo(title_entry, text_entry, tag_entry, register_window))
    register_button.grid(row=1, column=2, padx=20)

    return title_entry, text_entry, tag_entry

def register_memo(title_entry, text_entry, tag_entry, register_window):
    """メモ登録処理"""

    title = title_entry.get().strip()
    text = text_entry.get()
    tag = tag_entry.get()

    if title == "":
        messagebox.showerror("エラー", "タイトルを入力してください")
        return
    
    date_now = datetime.now().strftime("%Y/%m/%d %H:%M")

    memos = load_json()

    new_id = max((m["id"] for m in memos), default=0) + 1

    tags = [t.strip() for t in tag.split(",")]

    new_memo = {
        "id": new_id,
        "title": title,
        "text": text,
        "tags": tags,
        "day": date_now
    }

    memos.append(new_memo)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)
    
    messagebox.showinfo("追加成功", f"追加しました。追加日: {date_now}")
    register_window[0].destroy()

def search_memo_window(root, search_window):
    """メモ検索ウィンドウ"""
    if search_window[0] is not None and search_window[0].winfo_exists():
        search_window[0].lift()
        return
    else:
        search_window[0] = tk.Toplevel(root)
        search_window[0].title("メモ検索")
        search_window[0].geometry("700x300") #幅x高さ

    search_window[0].rowconfigure(0, weight=1)
    search_window[0].rowconfigure(2, weight=1)

    #タイトル・本文・タグの入力欄をグループ化
    search_frame = tk.Frame(search_window[0])
    search_frame.grid(row=1, sticky="w", padx=10)

    #タイトル
    title_label = tk.Label(search_frame, text="タイトル")
    title_label.grid(row=0, column=0, pady=10)

    title_entry = tk.Entry(search_frame, width=30)
    title_entry.grid(row=0, column=1)

    #本文
    text_label = tk.Label(search_frame, text="本文")
    text_label.grid(row=1, column=0, pady=10)

    text_entry = tk.Entry(search_frame, width=30)
    text_entry.grid(row=1, column=1)

    #タグ
    tag_label = tk.Label(search_frame, text="タグ")
    tag_label.grid(row=2, column=0, pady=10)

    tag_entry = tk.Entry(search_frame, width=30)
    tag_entry.grid(row=2, column=1)

    #検索ボタン
    search_button = tk.Button(search_frame, text="検索", command= lambda: search_memo(title_entry, text_entry, tag_entry, memo_list))
    search_button.grid(row=3, column=1)

    #メモ一覧の表示作成（Frameにてグループ化・スクロールバー追加）
    memo_list_frame = tk.Frame(search_window[0])
    memo_list_frame.grid(row=1, column=3)

    memo_list = tk.Listbox(memo_list_frame, width=70, height=15)
    scrollbar = tk.Scrollbar(memo_list_frame, orient="vertical", command=memo_list.yview)

    memo_list.configure(yscrollcommand=scrollbar.set)

    memo_list.grid(row=1, column=3)
    scrollbar.grid(row=1, column=4)

    #json読み込み・中身をlistboxにて表示
    memos = load_json()

    for m in memos:
        display = f"{m['id']}  |  {m['title']}  |  {m['text']}  |  {m['tags']}  |  {m['day']}"
        memo_list.insert(tk.END, display)

def search_memo(title_entry, text_entry, tag_entry, memo_list):
    """メモ検索処理"""
    memos = load_json()

    search_title = title_entry.get()
    search_text = text_entry.get()
    search_tags = tag_entry.get()

    memo_list.delete(0, tk.END)

    for m in memos:
        
        title_match = search_title == "" or search_title in m['title']
        text_match = search_text == "" or search_text in m['text']
        tags_match = search_tags == "" or search_tags in m['tags'] 

        if title_match and text_match and tags_match:
            search_display = f"{m['id']}  |  {m['title']}  |  {m['text']}  |  {m['tags']}  |  {m['day']}"
            memo_list.insert(tk.END, search_display)

def edit_memo_window(root, edit_window):
    """メモ編集・削除ウィンドウ"""
    if edit_window[0] is not None and edit_window[0].winfo_exists():
        edit_window[0].lift()
    else:
        edit_window[0] = tk.Toplevel(root)
        edit_window[0].title("メモ編集")
        edit_window[0].geometry("550x300")

    #左中央に設置
    edit_window[0].rowconfigure(0, weight=1)
    edit_window[0].rowconfigure(2, weight=1)
    edit_frame = tk.Frame(edit_window[0])
    edit_frame.grid(row=1, sticky="w", padx=30)

    #編集ボタン
    edit_info = [None]
    edit_button = tk.Button(edit_frame, text="編集", command=lambda: edit_memo(edit_window, edit_info, memo_list))
    edit_button.grid(row=0, column=0)

    #削除ボタン
    delete_button = tk.Button(edit_frame, text="削除", command=lambda: delete_memo(memo_list))
    delete_button.grid(row=1, column=0, pady=30)

    #メモ一覧
    memos = load_json()

    memo_list_frame = tk.Frame(edit_window[0])
    memo_list_frame.grid(row=1, column=3)

    #listboxにスクロールバーを追加(tk.Scrollbar)
    memo_list = tk.Listbox(memo_list_frame, width=70, height=15)
    scrollbar = tk.Scrollbar(memo_list_frame, orient="vertical", command=memo_list.yview)

    memo_list.configure(yscrollcommand=scrollbar.set)

    memo_list.grid(row=1, column=3)
    scrollbar.grid(row=1, column=4)

    #json読み込み・中身をlistboxに表示
    memos = load_json()

    for m in memos:
        display = f"{m['id']}  |  {m['title']}  |  {m['text']}  |  {m['tags']}  |  {m['day']}"
        memo_list.insert(tk.END, display)

def edit_memo(edit_window, edit_info, memo_list):
    """メモ編集処理"""
    index = memo_list.curselection()
    if not index:
        return
    else:
        memos = load_json()
        m = memos[index[0]]

    if edit_info[0] is not None and edit_info[0].winfo_exists():
        edit_info[0].lift()
    else:
        edit_info[0] = tk.Toplevel(edit_window[0])
        edit_info[0].title("編集")
        edit_info[0].geometry("300x80")

    #タイトル・本文・タグをフレーム化
    edit_info[0].rowconfigure(0, weight=1)
    edit_info[0].rowconfigure(2, weight=1)
    
    edit_frame = tk.Frame(edit_info[0])
    edit_frame.grid(row=1, sticky="w")

    #タイトル
    title_label = tk.Label(edit_frame, text="タイトル")
    title_label.grid(row=1, column=0)

    title_entry = tk.Entry(edit_frame, width=30)
    title_entry.grid(row=1, column=1)

    #本文
    text_label = tk.Label(edit_frame, text="内容")
    text_label.grid(row=2, column=0)

    text_entry = tk.Entry(edit_frame, width=30)
    text_entry.grid(row=2, column=1)

    #タグ
    tag_label = tk.Label(edit_frame, text="タグ")
    tag_label.grid(row=3, column=0)

    tag_entry = tk.Entry(edit_frame, width=30)
    tag_entry.grid(row=3, column=1)

    #タイトルの編集内容
    title_entry.delete(0, tk.END)
    title_entry.insert(0, m['title'])

    #本文の編集内容
    text_entry.delete(0, tk.END)
    text_entry.insert(0, m['text'])

    #タグの編集内容
    tag_entry.delete(0, tk.END)
    tag_entry.insert(0, ", ".join(m['tags']))

    #編集ボタン
    register_button = tk.Button(edit_info[0], text="編集", command=lambda: edit_complete(edit_info, m))
    register_button.grid(row=1, column=2, padx=20)

    def edit_complete(edit_info, m):
        """編集完了処理"""
        for memo in memos:
            if memo['id'] == m['id']:
                memo['title'] = title_entry.get()
                memo['text'] = text_entry.get()
                memo['tags'] = tag_entry.get().split(", ")
                break

        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(memos, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("編集完了", "編集しました。")
        edit_info[0].destroy()

        #編集後に画面更新
        memo_list.delete(0, tk.END)

        for m in memos:
            display = f"{m['id']}  |  {m['title']}  |  {m['text']}  |  {m['tags']}  |  {m['day']}"
            memo_list.insert(tk.END, display)

def delete_memo(memo_list):
    """メモ削除処理"""
    index = memo_list.curselection()

    if not index:
        return
    else:
        memos = load_json()
        m = memos[index[0]]
        select_delete = [memo for memo in memos if memo['id'] != m['id']]

    response = messagebox.askquestion("メモ削除", "選択したメモを削除しますか？")

    if response == "yes":
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(select_delete, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("削除完了", "選択したメモを削除しました。")

        #削除後に画面更新
        memo_list.delete(0, tk.END)

        for m in select_delete:
            display = f"{m['id']}  |  {m['title']}  |  {m['text']}  |  {", ".join(m['tags'])}  |  {m['day']}"
            memo_list.insert(tk.END, display)

    elif response == "no":
        return

    
if __name__ == "__main__":
    main()
