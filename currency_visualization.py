import pandas as pd
import os
import matplotlib.pyplot as plt

def generate_image():
  df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "jpy_krw.csv", engine="python")
  df_recent_currency = df.iloc[-24:, -1]

  plt.figure(figsize=(10, 5))

  df_recent_currency.plot()
  plt.gca().invert_yaxis()

  plt.title("recent 24 JPY/KRW currency")
  plt.xlabel("investigation index")
  plt.ylabel("KRW")

  plt.savefig(os.path.dirname(os.path.realpath(__file__)) + "/" + "recent_currency.png")
