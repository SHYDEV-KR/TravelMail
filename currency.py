import requests
import datetime as dt
import private.private as private
import time
import matplotlib.pyplot as plt
import os

import db

private_keys = private.my_keys()


def get_currencies(currency_code):
  body={
    "page_size": 30,
    "sorts": [
      {
        "property" : "date",
        "direction" : "descending"
      }
    ]
  }
  currency_queries = db.get_queries_from_database(private_keys["currency_db_id"], body=body)
  if currency_queries:
    currencies = []
    for query in currency_queries:
      date = query["properties"]["date"]["date"]["start"]
      currency = query["properties"][currency_code]["number"]
      currencies.append((date, currency))

  return currencies

def get_latest_currency(currency_code):
  body={
    "page_size": 1,
    "sorts": [
      {
        "property" : "date",
        "direction" : "descending"
      }
    ]
  }
  query = db.get_queries_from_database(private_keys["currency_db_id"], body=body)[0]
  date = query["properties"]["date"]["date"]["start"]
  currency = query["properties"][currency_code]["number"]
  return ({
    "date" : date,
    "currency" : currency,
  })

def save_image(currency_code):
  start = time.time()
  currencies = get_currencies(currency_code)
  date_list = [currencies[i - 1][0] for i in range(len(currencies), 0, -1)]
  currency_list = [currencies[i - 1][1] for i in range(len(currencies), 0, -1)]

  plt.figure(figsize=(15, 10))
  plt.plot(date_list, currency_list)
  plt.title(f"{currency_code}/KRW currency(recent 30 days)")
  plt.xlabel("date")
  plt.ylabel("KRW")
  plt.xticks(rotation=45)
  plt.savefig(os.path.dirname(os.path.realpath(__file__)) + "/img/" + f"recent_{currency_code.lower()}_currency.png")
  print(f"✅ successfully generated recent_{currency_code.lower()}_currency.png! (took {round(time.time() - start, 3)}s)")


def get_currency_data(currency_code, date=dt.datetime.today()):
  url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={private_keys['currency_api_key']}&searchdate={date.year}{str(date.month).zfill(2)}{str(date.day).zfill(2)}&data=AP01"
  currencies_response = requests.get(url).json()
  if currencies_response == []:
    return False

  for currency in currencies_response:
    if currency["cur_unit"][:3] == currency_code:
      return float(currency["deal_bas_r"].replace(",",""))


if __name__ == "__main__":
  currencies = dict()
  date = dt.datetime.today()
  available_currency_list = ["JPY", "USD"]

  for currency_code in available_currency_list:
    start = time.time()
    currency_data = get_currency_data(currency_code, date=date)
    if currency_data:
      currencies[currency_code] = currency_data
      print(f"✅ updated latest {currency_code}_KRW currency! (took {round(time.time() - start, 3)}s)")
    else:
      print(f"❌ {date} : Not a weekday or date is invalid!")
      break

  if currencies:
    try:
      db.generate_new_page_in_currency_db(private_keys["currency_db_id"], currencies, date=date)
      for currency_code in available_currency_list:
        save_image(currency_code)
    except:
      raise