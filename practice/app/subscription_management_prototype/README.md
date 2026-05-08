# subscription_management_prototype

## 概要
- 定額サービス（サブスク）の利用状況を管理するアプリのプロトタイプです。

## 機能
- 現在利用している定額サービスの登録
- 年額・月額の料金の集計（円グラフで表示）
- 登録済定額サービス一覧の表示

## 使い方
1. `main.py`を実行
2. 下部のボタンを操作（登録・集計(月額)・集計(年額)・一覧）
3. 処理完了時にcsvファイルに保存される

## 必要なもの
- Python 3.12.10
- ttkbootstrap  (インストールコマンド: `pip install ttkbootstrap`)
- matplotlib    (インストールコマンド: `pip install matplotlib`)
- pandas        (インストールコマンド: `pip install pandas`)

## ファイル構成
```
subscription_management_prototype/
├── data/
│   └── subscription.csv    # 記録データ
├── main.py     # メインプログラム
└── README.md   # アプリの説明（当ファイル）
```