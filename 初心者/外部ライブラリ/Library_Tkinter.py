#Tkinter（読み方：ティーケーインター）専用ウィンドウを作成する外部ライブラリ　VBAでいうユーザーフォームみたいなやつ
import tkinter as tk

#ウィンドウ作成
root = tk.Tk()
root.title("初めてのTKinter")
root.geometry("300x200")

#ラベル作成
label = tk.Label(root, text="こんにちは")
label.pack()

#ボタンが押されたときの処理
def click_button():
    label.config(text="ボタンが押されました")

#ボタン作成
button =tk.Button(root, text="押す", command=click_button)
button.pack()

#アプリ起動
root.mainloop()