import requests
import datetime as dt
import pandas as pd
import private.private as private
import os
import time
from currency_visualization import save_image

def get_currency_data(date_time, currency_code):
  url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={private.my_keys()['currency_api_key']}&searchdate={date_time.year}{str(date_time.month).zfill(2)}{str(date_time.day).zfill(2)}&data=AP01"
  currencies_response = requests.get(url).json()
  if currencies_response == []:
    return False

  for currency in currencies_response:
    if currency["cur_unit"][:3] == currency_code:
      return [f'{date_time.year}-{str(date_time.month).zfill(2)}-{str(date_time.day).zfill(2)}', f'{str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}:{str(now.second).zfill(2)}', float(currency["deal_bas_r"].replace(",",""))]


for currency_code in ["JPY", "USD"]:
  start = time.time()
  df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/csv/" + f"{currency_code.lower()}_krw.csv", engine='python')
  length = df.shape[0] + 1
  now = dt.datetime.now()
  currency_data = get_currency_data(now, currency_code)
  if currency_data:
    df.loc[length] = currency_data
    df.to_csv(os.path.dirname(os.path.realpath(__file__)) + "/csv/" + f"{currency_code.lower()}_krw.csv", index=False)
    print(f"✅ updated latest {currency_code}_KRW currency! (took {round(time.time() - start, 3)}s)")
    save_image(currency_code)
  else:
    print("❌ today is not a weekday!")