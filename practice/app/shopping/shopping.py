from datetime import datetime

cart = []

def add_item():
    """商品と値段を記入し、追加する（無制限）。"""
    while True:
        product = input("商品名: ").strip()
        if product == "":
            print("商品名を入力してください")
            continue
        break

    while True:    
        try:
            price = int(input("単価: "))
        except ValueError:
            print("数字を入力してください")
            continue
        if price == 0:
            print("単価を設定してください")
            continue
        try:
            qty = int(input("個数: "))
        except ValueError:
            print("数字を入力してください")
            continue
        break

    cart.append(
        {"商品名": product, "数量": qty, "値段": price} #商品を複数追加可能
    )

    print("\nカートに追加しました。")
    print(f"商品名:{product}  単価:￥{price:,}")
    print("\nカートの中身")

    for item in cart:
        print(f"商品名: {item['商品名']} / 数量: {item['数量']} / 値段: ￥{item['値段'] * item['数量']:,}")
    return

def check_in():
    """お会計（合計金額が5,000円以上なら10%割引）"""

    total = sum(item['値段']for item in cart)  # 値段の合計

    print("=" * 40)
    print("お会計(￥5,000以上なら10%割引します)")
    print("=" * 40)
    print(f"購入日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")

    if total >= 5000:
        sale = total * 0.1
        pay = total - sale
    else:
        sale = 0
        pay = total

    for item in cart:
        print(f"{item['商品名']:<5} x {item['数量']:<5} ￥{item['値段'] * item['数量']:,}")

    print(f"\n合計  ￥{pay:,}")
    print(f"割引  ￥{sale:,}")

def main():
    """メイン画面"""
    while True:
        print("=" * 16)
        print("お買い物システム")
        print("=" * 16)

        print("1) 買い物をする")
        print("2) お会計")
        print("3) 終了")

        choice = input("選択: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            if not cart:
                print("カートが空です")
                continue
            check_in()
        elif choice == "3":
            print("終了します")
            break
        else:
            print("1~3のいずれかを入力してください")
            continue 

if __name__ == "__main__":
    main()