import time # sleep 활용을 위해
from selenium import webdriver 
from bs4 import BeautifulSoup

import pandas as pd

def arrangeFlightData(dataList: list):
  df = list()
  for d in dataList:
    d[0].append(d[-1])
    d[1].append("-")
    df.append(d[0])
    df.append(d[1])
    df.append(["-"] * 6)
  
  df = pd.DataFrame(df, columns=['항공사', '출발', '소요시간', '도착', '종류', '총 가격'])
  df_html = df.to_html(index=False, justify='center')
  df_html = df_html.replace('<table border="1" class="dataframe">', '<table border="0" class="dataframe" bgcolor=black cellpadding=1 cellspacing=1><tr><td><table border="0" class="dataframe" bgcolor=black>')
  df_html = df_html.replace('</table>', '</table> </td></tr></table>')
  df_html = df_html.replace('<td>','<td bgcolor=white>')
  df_html = df_html.replace('<th>','<th bgcolor=#B1B2FF>')
  return df_html


def getFlightData(url):
  specific_options = webdriver.ChromeOptions()
  specific_options.add_argument('--headless')
  specific_options.add_argument('--no-sandbox')

  driver = webdriver.Chrome('chromedriver', options = specific_options)
  driver.set_window_size(1920, 1080)
  driver.get(url)
  time.sleep(3)
  driver.save_screenshot('price.png')

  result = []

  soup = BeautifulSoup(driver.page_source, 'html.parser')
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

  return arrangeFlightData(result)