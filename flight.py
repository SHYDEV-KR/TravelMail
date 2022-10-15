import time # sleep 활용을 위해
from selenium import webdriver 
from bs4 import BeautifulSoup

import pandas as pd
import os

def arrange_flight_data(data_list: list):
  start = time.time()
  df = list()
  for d in data_list:
    d[0].append(d[-1])
    d[1].append("-")
    df.append(d[0])
    df.append(d[1])
    df.append(["-"] * 6)
  
  for i, d in enumerate(df):
    if len(d) > 6:
      df[i] = d[1:]

  df = pd.DataFrame(df, columns=['항공사', '출발', '소요시간', '도착', '종류', '총 가격'])
  df_html = df.to_html(index=False, justify='center')
  df_html = df_html.replace('<table border="1" class="dataframe">', '<table border="0" class="dataframe" bgcolor=black cellpadding=1 cellspacing=1><tr><td><table border="0" class="dataframe" bgcolor=black>')
  df_html = df_html.replace('</table>', '</table> </td></tr></table>')
  df_html = df_html.replace('<td>','<td bgcolor=white>')
  df_html = df_html.replace('<th>','<th style="color: white;" bgcolor=#B1B2FF>')
  print(f"✅ successfully arranged flight data! (took {round(time.time() - start, 3)}s)")
  return df_html


def get_flight_data(url):
  start = time.time()
  specific_options = webdriver.ChromeOptions()
  specific_options.add_argument('--headless')
  specific_options.add_argument('--no-sandbox')

  driver = webdriver.Chrome('chromedriver', options = specific_options)
  driver.set_window_size(1920, 1080)
  driver.get(url)
  time.sleep(3)
  driver.save_screenshot(os.path.dirname(os.path.realpath(__file__)) + "/img/" + 'price.png')

  # 스크롤 처리
  scroll_location = driver.execute_script("return document.body.scrollHeight")
  cnt = 0
  while cnt < 1:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    if scroll_location == scroll_height:
      break
    else:
      scroll_location = driver.execute_script("return document.body.scrollHeight")
      cnt += 1
  result = []

  soup = BeautifulSoup(driver.page_source, 'html.parser')
  todays_flight = int(soup.find(role="resultCount").text)

  for i, e in enumerate(soup.find_all("div", class_="mrt_foreign_wrap k1_clearfix")):
    result.append([])
    result[i] = [string.text.strip("\n ") for string in e.find_all("div", class_="list")]
    result[i].append(e.find("span", class_="fare_total").text)
    result[i][0] = result[i][0].split("\n")
    result[i][1] = result[i][1].split("\n")

  result = result[1:]

  for r in result:
    for i in range(len(r)):
      count = 0
      for j in range(len(r[i])):
        if '' == r[i][j]:
          count += 1
      
      for _ in range(count):
        r[i].remove('')
  print(f"✅ successfully received flight data from url! (took {round(time.time() - start, 3)}s)")
  return todays_flight, arrange_flight_data(result)