import re
import tkinter as tk
from tkinter import filedialog, messagebox
from spellchecker import SpellChecker

def pick_file():
    path = filedialog.askopenfilename(
        title="テキストファイルを選択",
        filetypes=[("Text Files", "*.txt"),("All files","*.*")]
    )
    
    if not path:
        raise
    
    try:
        with open(path, "r",encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        messagebox.showerror("読み込みエラー", str(e))
        raise

    #英単語だけ抽出（a-zの連続）
    words=re.findall(r"[A-Za-z']+",text)

    spell = SpellChecker()
    misspelled = spell.unknown(words)

    #表示を更新
    listbox.delete(0, tk.END)

    if not misspelled:
        listbox.insert(tk.END,"誤字候補は見つかりませんでした。")
        raise

    for w in sorted(misspelled):
        suggestions = ", ".join(list(spell.candidates(w))[:5])
        listbox.insert(tk.END,f"{w} -> 候補;{suggestions}")

#--- GUI ---
root = tk.Tk()
root.title("誤字脱字チェックアプリ")
root.geometry("700x400")

btn = tk.Button(root,text="テキストファイルを選択してください", command=pick_file)
btn.pack(pady=10)

listbox=tk.Listbox(root,width=100,height=18)
listbox.pack(padx=10,pady=10, fill=tk.BOTH, expand=True)

root.mainloop()