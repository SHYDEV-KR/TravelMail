from locale import currency
import requests
import datetime as dt
import pandas as pd
import private
import os

def getCurrencyData():
  now = dt.datetime.now()
  url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={private.myKeys()['currency_api_key']}&searchdate={now.year}{str(now.month).zfill(2)}{str(now.day).zfill(2)}&data=AP01"
  currencies_response = requests.get(url).json()
  if currencies_response == []:
    return False

  if currencies_response[12]["cur_unit"] == "JPY(100)":
    JPY_KRW = currencies_response[12]["deal_bas_r"]
  else:
    for currency in currencies_response:
      if currency["cur_unit"] == "JPY(100)":
        JPY_KRW = currency["deal_bas_r"]
        break
  
  return [f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}', f'{str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}:{str(now.second).zfill(2)}', JPY_KRW]


df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "jpy_krw.csv", engine='python')
length = df.shape[0] + 1
currency_data = getCurrencyData()
if currency_data:
  df.loc[length] = currency_data
  df.to_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "jpy_krw.csv", index=False)
  print("✅ updated latest currency!")
else:
  print("❌ today is not a weekday!")