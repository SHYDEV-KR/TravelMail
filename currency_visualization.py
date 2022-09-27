import pandas as pd
import os
import matplotlib.pyplot as plt

def generate_image():
  df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "jpy_krw.csv", engine="python")
  df_recent_currency = df.iloc[-24:, -1]

  plt.figure(figsize=(10, 5))

  df_recent_currency.plot()
  plt.gca().invert_yaxis()

  plt.title("JPY/KRW currency(recent day)")
  plt.xlabel("time")
  plt.ylabel("KRW")
  plt.gca().axes.xaxis.set_visible(False)

  plt.savefig(os.path.dirname(os.path.realpath(__file__)) + "/" + "recent_currency.png")