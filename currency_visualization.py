import time
import pandas as pd
import os
import matplotlib.pyplot as plt

def save_image(currency_code):
  start = time.time()
  df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/csv/" + f"{currency_code.lower()}_krw.csv", engine="python")
  df_recent = df.iloc[-30:]

  plt.figure(figsize=(15, 10))
  plt.plot(df_recent["date"], df_recent["currency"])
  plt.title(f"{currency_code}/KRW currency(recent 30 days)")
  plt.xlabel("date")
  plt.ylabel("KRW")
  plt.xticks(rotation=45)
  plt.savefig(os.path.dirname(os.path.realpath(__file__)) + "/img/" + f"recent_{currency_code.lower()}_currency.png")
  print(f"✅ successfully generated recent_{currency_code.lower()}_currency.png! (took {round(time.time() - start, 3)}s)")