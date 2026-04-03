#matplotlib　グラフを作成する外部ライブラリ
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

plt.bar(df["name"], df["score"])
plt.show()