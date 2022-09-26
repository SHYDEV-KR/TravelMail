import time
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import private

def getCurrencyData(url):
  specific_options = webdriver.ChromeOptions()
  specific_options.add_argument('--headless')
  specific_options.add_argument('--no-sandbox')

  driver = webdriver.Chrome('chromedriver', options = specific_options)
  driver.set_window_size(1920, 1080)
  driver.get(url)
  time.sleep(3)
  JPY_KRW = round(float(driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div/div[2]/main/div/div[1]/div[2]/div[1]/span').text) * 100, 2)
  
  now = dt.datetime.now()
  return [f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}', f'{str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}:{str(now.second).zfill(2)}', JPY_KRW]


df = pd.read_csv("jpy_krw.csv", engine='python')
length = df.shape[0] + 1
df.loc[length] = getCurrencyData(private.info["currency_url"])
df.to_csv("jpy_krw.csv", index=False)