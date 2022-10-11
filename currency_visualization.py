import pandas as pd
import os
import matplotlib.pyplot as plt

def generate_image():
  df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "jpy_krw.csv", engine="python")
  df_recent = df.iloc[-10:]

  plt.figure(figsize=(15, 10))
  plt.plot(df_recent["date"], df_recent["currency"])
  plt.title("JPY/KRW currency(recent 10days)")
  plt.xlabel("date")
  plt.ylabel("KRW")
  plt.xticks(rotation=45)
  plt.savefig(os.path.dirname(os.path.realpath(__file__)) + "/" + "recent_currency.png")