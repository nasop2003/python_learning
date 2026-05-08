import pandas as pd
from pathlib import Path
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

FILE_PATH_CSV = Path(__file__).parent / "data" / "subscription.csv"

root = tb.Window(themename="darkly")
root.title("サブスク管理")
root.geometry("600x400") #幅x高さ

notebook = tb.Notebook(root, bootstyle="light")
notebook.pack(pady=20)

#tb.frame
tab_sublist = None
tab_summary_m = None
tab_summary_y = None

#tb.Treeview
tree = None

#matplotlib(月額)
fig_m = None
ax_m = None
canvas_m = None

#matplotlib(年額)
fig_y = None
ax_y = None
canvas_y = None

def init_csv() -> None:
    """csvが存在しない場合のみ初期化"""
    if not Path(FILE_PATH_CSV).exists():
        pd.DataFrame(columns=["サービス名", "料金", "初回支払日", "支払形式"]).to_csv(
            FILE_PATH_CSV, index=False, encoding="utf-8-sig"
        ) 
    print("csvファイルを新規作成しました")

def save_csv(data_csv: str) -> None:
    """登録時に１行追記する"""
    df = pd.DataFrame(
        [data_csv],
        columns=["サービス名", "料金", "初回支払日", "支払形式"]
    )
    
    df.to_csv(FILE_PATH_CSV, index=False, encoding="utf-8-sig", mode="a", header=False)
    print("csvファイルの書き込みが完了しました")

def create_tab() -> tuple[tb.Frame, tb.Frame, tb.Frame]:
    """各タブ追加"""
    #集計（月額）
    tab_summary_m = tb.Frame(notebook, width=580, height=350)
    notebook.add(tab_summary_m, text="集計（月額）")
    
    #集計（年額）
    tab_summary_y = tb.Frame(notebook, width=580, height=350)
    notebook.add(tab_summary_y, text="集計（年額）")
    
    #サブスク一覧
    tab_sublist = tb.Frame(notebook, width=580, height=350)
    notebook.add(tab_sublist, text="一覧")
    
    return tab_summary_m, tab_summary_y, tab_sublist

def summary_month(tab_summary_m):
    """集計画面（月額）"""
    global fig_m, ax_m, canvas_m
    df = pd.read_csv(FILE_PATH_CSV)
    
    month = df[df["支払形式"] == "月額"]
    year = df[df["支払形式"] == "年額"]

    total = month["料金"].sum() + (year["料金"] // 12).sum()
    
    print(f"登録済サービスの料金（月額）: {total:,}")
    
    fig_m = Figure(figsize=(5.8, 3.5)) #横インチ・縦インチ
    ax_m = fig_m.add_subplot(1, 1, 1)
        
    fig_m.suptitle(f"合計: ￥{total:,}", fontfamily="MS Gothic")
    
    monthly_prices = df["料金"].copy()
    monthly_prices[df["支払形式"] == "年額"] = monthly_prices[df["支払形式"] == "年額"] // 12
    
    #グラフ内容
    ax_m.pie(
        monthly_prices,
        autopct="%1.1f%%",
    )
    
    
    #凡例
    ax_m.legend(
        labels= df["サービス名"],
        bbox_to_anchor= (0.9, 1), #横x縦
        loc= "upper left",
        fontsize= "small",
        handlelength= 3
    )  
    
    canvas_m = FigureCanvasTkAgg(fig_m, master=tab_summary_m)
    canvas_m.draw()
    canvas_m.get_tk_widget().place(x=1, y=1)

def summary_month_update() -> None:
    """グラフ更新（月額）"""
    df = pd.read_csv(FILE_PATH_CSV)
    
    ax_m.clear()
    
    monthly_prices = df["料金"].copy()
    monthly_prices[df["支払形式"] == "年額"] = monthly_prices[df["支払形式"] == "年額"] // 12
    
    ax_m.pie(
        monthly_prices,
        autopct="%1.1f%%",
    )
    
    ax_m.legend(
        labels= df["サービス名"],
        bbox_to_anchor= (0.9, 1), #横x縦
        loc= "upper left",
        fontsize= "small",
        handlelength= 3
    )  
    
    canvas_m.draw()
    
def summary_year(tab_summary_y) -> None:
    
    """集計画面（年額）"""
    global fig_y, ax_y, canvas_y
    df = pd.read_csv(FILE_PATH_CSV)
    print(df.dtypes)
    
    month = df[df["支払形式"] == "月額"]
    year = df[df["支払形式"] == "年額"]
    
    total = (month["料金"] * 12).sum() + year["料金"].sum()
    
    print(f"登録済サービスの料金（年額）: {total:,}")
    
    fig_y = Figure(figsize=(5.8, 3.5)) #横インチ・縦インチ
    ax_y = fig_y.add_subplot(1, 1, 1)
    
    fig_y.suptitle(f"合計: ￥{total:,}", fontfamily="MS Gothic")
    
    yearly_prices = df["料金"].copy()
    yearly_prices[df["支払形式"] == "月額"] = yearly_prices[df["支払形式"] == "月額"] * 12
    
    #グラフ内容
    ax_y.pie(
        yearly_prices,
        autopct="%1.1f%%"
    )
    
    
    #凡例
    ax_y.legend(
        labels= df["サービス名"],
        bbox_to_anchor= (0.9, 1), #横x縦
        loc= "upper left",
        fontsize= "small",
        handlelength= 3
    )  
    
    canvas_y = FigureCanvasTkAgg(fig_y, master=tab_summary_y)
    canvas_y.draw()
    canvas_y.get_tk_widget().place(x=1, y=1)
    
def summary_year_update() -> None:
    """グラフ更新（年額）"""
    df = pd.read_csv(FILE_PATH_CSV)
    
    ax_y.clear()
    
    yearly_prices = df["料金"].copy()
    yearly_prices[df["支払形式"] == "月額"] = yearly_prices[df["支払形式"] == "月額"] * 12
    
    ax_y.pie(
        yearly_prices,
        autopct="%1.1f%%"
    )

    ax_y.legend(
        labels= df["サービス名"],
        bbox_to_anchor= (0.9, 1), #横x縦
        loc= "upper left",
        fontsize= "small",
        handlelength= 3
    )  
    
    canvas_y.draw()
    
def sub_list(tab_sublist) -> None:
    """サブスク一覧"""
    global tree
    df = pd.read_csv(FILE_PATH_CSV)
    
    tree = tb.Treeview(tab_sublist)
    
    tree["columns"] = ("サービス名", "料金", "初回支払日", "支払形式")
    
    tree.column("#0", width=30, stretch=False)
    tree.column("サービス名", width=150, anchor=CENTER, stretch=False)
    tree.column("料金", width=70, anchor=CENTER, stretch=False)
    tree.column("初回支払日", width=170, anchor=CENTER, stretch=False)
    tree.column("支払形式", width=90, anchor=CENTER, stretch=False)

    tree.heading("#0", text="")
    tree.heading("サービス名", text="サービス名")
    tree.heading("料金", text="料金")
    tree.heading("初回支払日", text="初回支払日")
    tree.heading("支払形式", text="支払形式")
    
    def block_resize(event):
        if tree.identify_region (event.x, event.y) == "separator":
            return "break"
        
    tree.bind("<Button-1>", block_resize)
    tree.bind("<B1-Motion>", block_resize)
    
    for row in df.itertuples():
        tree.insert(parent="", index="end", iid=None, values=(row[1], f"￥{row[2]:,}", row[3], row[4]))
    
    tree.place(x=0, y=60, width=580)

def sub_list_update() -> None:
    """サブスク一覧画面更新"""
    df = pd.read_csv(FILE_PATH_CSV)
    
    for row in tree.get_children():
        tree.delete(row)
    
    for row in df.itertuples():
        tree.insert(parent="", index="end", iid=None, values=(row[1], f"￥{row[2]:,}", row[3], row[4]))

def sub_create() -> tb.StringVar:
    """サブスク情報登録画面"""
    tab_sub = tb.Frame(notebook, width=580, height=350)
    notebook.add(tab_sub, text="登録")
    
    PIXEL_X = 150
    
    txt1 = tb.Label(tab_sub, text="サービス名")
    txt1.place(x=PIXEL_X, y=45)

    txt2 = tb.Label(tab_sub, text="料金")
    txt2.place(x=PIXEL_X, y=85)
    
    txt3 = tb.Label(tab_sub, text="初回支払日")
    txt3.place(x=PIXEL_X, y=125)
    
    txt4 = tb.Label(tab_sub, text="月額/年額")
    txt4.place(x=PIXEL_X, y=165)
    
    def on_change(*args):
        """全項目入力時にボタンが押せるように設定する処理"""
        if var1.get() and var2.get() and var3.get() and var4.get():
            button.config(state=NORMAL, bootstyle=PRIMARY)
        else:
            button.config(state=DISABLED, bootstyle=SECONDARY)
    
    def only_digits(value) -> bool:
        """数字入力のみ受け付け"""
        return value.isdigit() or value == ""

    #tb.Comboboxのウィンドウ幅と揃えたいため調整
    WIDGET_WIDTH = 22
    
    #サービス名
    var1 = tb.StringVar()
    var1.trace_add("write", on_change)
    txt1_entry = tb.Entry(tab_sub, width=WIDGET_WIDTH)
    txt1_entry.config(textvariable=var1)
    txt1_entry.place(x=280, y=40)

    #料金
    var2 = tb.StringVar()
    var2.trace_add("write", on_change)
    txt2_vcmd = (tab_sub.register(only_digits), "%P")
    txt2_entry = tb.Entry(tab_sub, width=WIDGET_WIDTH)
    txt2_entry.config(validate="key", validatecommand=txt2_vcmd, textvariable=var2)
    txt2_entry.place(x=280, y=80)
    
    #初回支払日（カレンダー選択）
    var3 = tb.StringVar()
    var3.trace_add("write", on_change)
    txt3_entry = tb.DateEntry(tab_sub, width=WIDGET_WIDTH, dateformat="%Y-%m-%d")
    txt3_entry.entry.config(textvariable=var3)
    txt3_entry.entry.bind("<Key>", lambda e: "break")
    txt3_entry.place(x=280, y=120)
    
    #月額/年額
    var4 = tb.StringVar()
    var4.trace_add("write", on_change)
    txt4_combobox = tb.Combobox(tab_sub)
    txt4_combobox.config(values=["月額", "年額"], state=READONLY ,textvariable=var4)
    txt4_combobox.place(x=280, y=160)
    
    button = tb.Button(tab_sub, text="登録", state=DISABLED ,bootstyle=SECONDARY,  command=lambda:sub_processing(var1, var2, var3, var4))
    button.place(x=260, y=220)
    
def sub_processing(var1, var2, var3, var4: tb.StringVar) -> None:
    """サブスク情報登録処理"""
    print("登録しました")
    print(f"{var1.get()} / {var2.get()} / {var3.get()} / {var4.get()}")
    
    name = var1.get()
    price = int(var2.get())
    pay_day = var3.get()
    pay_method = var4.get()

    write_csv = [name, price, pay_day, pay_method]
    
    save_csv(write_csv)
    messagebox.showinfo("登録完了", "登録が完了しました。")

    var1.set("")
    var2.set("")
    var3.set("")
    var4.set("")
    
    sub_list_update()
    summary_month_update()
    summary_year_update()
    
def main():
    global tab_sublist, tab_summary_m, tab_summary_y
    init_csv()
    
    sub_create()
    tab_summary_m, tab_summary_y, tab_sublist = create_tab()
    summary_month(tab_summary_m)
    summary_year(tab_summary_y)
    sub_list(tab_sublist)
    
if __name__ == "__main__":
    main()
    root.mainloop()