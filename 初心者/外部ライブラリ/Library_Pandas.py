#pandas　データを取り扱う外部ライブラリ
import pandas as pd

df = pd.read_csv("data.csv")

print(df)
print("平均点:", df["score"].mean())