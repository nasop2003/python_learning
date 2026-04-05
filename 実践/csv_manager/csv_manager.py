import csv
from pathlib import Path

#設定
CSV_PATH = Path("Python_csv.csv")
FIELDS = ["id", "name", "email"] #列名（自由に変えてOK）

def load_csv(path: Path) -> list[dict]:
    """CSVを読み込んで、dictのリストで返す。なければ空で返す。"""
    if not path.exists():
        return []
    
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    #欠けている例があっても最低限は揃える
    for r in rows:
        for field in FIELDS:
            r.setdefault(field,"")
    return rows

def save_csv(path: Path, rows: list[dict]) -> None:
    """dictのリストをCSVに保存する（上書き）。"""
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def ensure_csv_exists(path: Path) -> None:
    """CSVが無ければヘッダーだけ作る。"""
    if path.exists():
        return
    save_csv(path,[])

def next_id(rows: list[dict]) -> str:
    """idの最大値+1 を文字列で返す(idが数字でない行は無視)。"""
    max_id = 0
    for r in rows:
        try:
            max_id = max(max_id, int(r.get("id", "").strip()))
        except ValueError:
            pass
    return str(max_id + 1)

def search_rows(rows:list[dict], keyword: str) -> list[dict]:
    """全列からキーワードを部分一致検索（大文字小文字無視）。"""
    kw = keyword.strip().lower()
    if not kw:
        return []
    
    results = []
    for r in rows:
        joined = " ".join(str(r.get(f,"")) for f in FIELDS).lower()
        if kw in joined:
            results.append(r)
    return results

def print_rows(rows: list[dict]) -> None:
    """見やすく表示（簡易）"""
    if not rows:
        print("(該当なし)")
        return
    
    #ヘッダー表示
    print("-" * 60)
    print(" | ".join(FIELDS))
    print("-" * 60)

    for r in rows:
        line = " | ".join(str(r.get(f,"")) for f in FIELDS)
        print(line) 

    print("-" * 60)
    print(f"{len(rows)}件")

def add_row(rows: list[dict]) -> None:
    """ユーザー入力で１行追加（メモリ上に追加するだけ）。"""
    new = {}
    new["id"] = next_id(rows)

    print("追加するデータを入力してください（空でもOK）")
    for field in FIELDS:
        if field == "id":
            continue
        new[field] = input(f"{field}:").strip()

    rows.append(new)
    print(f"追加しました: {new}")

def menu() -> None:
    ensure_csv_exists(CSV_PATH)
    rows = load_csv(CSV_PATH)

    while True:
        print("\n=== CSVデータ管理 ===")
        print("1) 全件表示")
        print("2) 検索")
        print("3) 追加")
        print("4) 保存")
        print("5) 終了")
        choice = input("選択: ").strip()

        if choice == "1":
            print_rows(rows)
        
        elif choice == "2":
            keyword = input("検索キーワード: ")
            results = search_rows(rows, keyword)
            print_rows(results)

        elif choice == "3":
            add_row(rows)

        elif choice == "4":
            save_csv(CSV_PATH, rows)
            print(f"保存しました: {CSV_PATH.resolve()}")

        elif choice == "5":
            #終了前に保存するか確認（初心者向けに安全）
            ans = input("保存して終了しますか？（y/n): ").strip().lower()
            if ans == "y":
                save_csv(CSV_PATH, rows)
                print("保存して終了しました。")
            else:
                print("保存せず終了しました。")
            break

        else:
            print("1～5で選んでください。")

if __name__ == "__main__":
    menu()