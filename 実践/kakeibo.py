from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Dict

CSV_PATH = Path("kakeibo.csv")
DATE_FMT = "%Y-%m-%d"

@dataclass
class Record:
    day: date
    kind: str
    category: str
    amount: int
    memo: str = ""

def ensure_csv_header() -> None:
    """CSVが存在しなければヘッダー付きで作る"""
    if CSV_PATH.exists():
        return
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "kind", "category", "amount", "memo"])

def parse_date(s: str) -> date:
    return datetime.strptime(s, DATE_FMT).date()

def input_date(prompt: str) -> date:
    while True:
        s = input(prompt).strip()
        try:
            return parse_date(s)
        except ValueError:
            print("日付の形式が違います。例: 2026-02-27")

def input_kind() -> str:
    while True:
        s = input("種別を入力（1:支出 / 2:収入）: ").strip()
        if s == "1":
            return "expense"
        elif s == "2":
            return "income"
        else:
            print("1か2を入力してください")

def input_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        try:
            x = int(s)
            if x <= 0:
                print("1以上の金額を入力してください")
                continue
            return x
        except ValueError:
            print("数字を入力してください")

def add_record() -> None:
    day = input_date("日付（YYYY-MM-DD）: ")
    kind = input_kind()
    category = input("カテゴリ（例：食費/交通/給料/）: ").strip() or "未分類"
    amount = input_int("金額（整数）: ")
    memo = input("メモ（任意）: ").strip()

    rec = Record(day=day, kind=kind, category=category, amount=amount, memo=memo)

    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([rec.day.strftime(DATE_FMT), rec.kind, rec.category, rec.amount, rec.memo])

    print("追加しました")

def load_records() -> List[Record]:
    ensure_csv_header()
    records: list[Record] = []
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            records.append(
                Record(
                    day=parse_date(row["date"]),
                    kind=row["kind"],
                    category=row["category"],
                    amount=int(row["amount"]),
                    memo=row.get("memo", "") or "",
                )
            )
    return records

def print_records(records: List[Record]) -> None:
    if not records:
        print("(データなし)")
        return
    
    print("-" * 72)
    print(f"{"date":10} {"kind":7} {"category":10} {"amount":10} memo")
    print("-" * 72)
    for rec in records:
        print(
            f"{rec.day.strftime(DATE_FMT):10} {rec.kind:7} {rec.category[:10]:10}"
            f"{rec.amount:10} {rec.memo}"
        )
    print("-" * 72)

def list_all() -> None:
    records = load_records()
    print_records(records)

def search_records() -> None:
    records = load_records()

    print("検索結果を入力（空ならスキップ）")
    start: Optional[date] = None
    end: Optional[date] = None

    s1 = input("開始日（YYYY-MM-DD）: ").strip()
    if s1:
        try:
            start = parse_date(s1)
        except ValueError:
            print("開始日の形式が違うのでスキップします")

    s2 = input("終了日（YYYY-MM-DD）: ").strip()
    if s2:
        try:
            end = parse_date(s2)
        except ValueError:
            print("終了日の形式が違うのでスキップします")
    
    category = input("カテゴリ（例: 食費) : ").strip()
    kind_in = input("種別（expense/income) : ").strip()

    filtered: List[Record] = []
    for rec in records:
        if start and rec.day < start:
            continue
        if end and rec.day > end:
            continue
        if category and rec.category != category:
            continue
        if kind_in and rec.kind != kind_in:
            continue
        filtered.append(rec)

def summerize_monthly() -> None:
    records = load_records()
    by_month: Dict[str, Dict[str, int]] = {}

    for rec in records:
        key = rec.day.strftime("%Y-%m")
        by_month.setdefault(key,{"income": 0, "expense": 0})
        by_month[key][rec.kind] += rec.amount

    if not by_month:
        print("(データなし)")
        return
    
    print("-" * 48)
    print(f"{"month":7} {"income":12} {"expense":12} {"balance":12}")
    print("-" * 48)

    for m in sorted(by_month.keys()):
        inc = by_month[m]["income"]
        exp = by_month[m]["expense"]
        bal = inc - exp
        print(f"{m:7} {inc:12} {exp:12} {bal:12}")

    print("-" * 48)

def summerize_by_category() -> None:
    records = load_records()
    totals: Dict[str, int] = {}

    for rec in records:
        if rec.kind != "expense":
            continue
        totals[rec.category] = totals.get(rec.category, 0) + rec.amount
    
    if  not totals:
        print("(支出データなし)")
        return

    print("-" * 36)
    print(f"{"category":12} {"expense_total":12}")
    print("-" * 36)
    for cat, total in sorted(totals.items(), key= lambda x: x[1], reverse=True):
        print(f"{cat[:12]:12} {total:12}")
    print("-" * 36)

def main() -> None:
    ensure_csv_header()

    while True:
        print("\n=== 家計簿アプリ ===")
        print("1) 追加")
        print("2) 一覧表示")
        print("3) 検索")
        print("4) 月別集計")
        print("5) カテゴリ別集計(支出)")
        print("0) 終了")

        choice = input("選択: ").strip()

        if choice == "1":
            add_record()
        elif choice == "2":
            list_all()
        elif choice == "3":
            search_records()
        elif choice == "4":
            summerize_monthly()
        elif choice == "5":
            summerize_by_category
        elif choice == "0":
            print("終了します")
            break
        else:
            print("0~5を入力してください")

if __name__ == "__main__":
    main()
        