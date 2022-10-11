import flight
import currency_visualization

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import datetime as dt
import private
import os
import pandas as pd

df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "jpy_krw.csv", engine='python')
length = df.shape[0]
currency_visualization.generate_image()
privateKeys = private.myKeys()
try:
  yesterdayFlights = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "yesterday_flight.csv").shape[0]
except:
  yesterdayFlights = 0
todayFlights, flightTable = flight.getFlightData(privateKeys["url"])
recipients = privateKeys["recipients"]
message = MIMEMultipart()
message['Subject'] = f'[{dt.datetime.now().month}월 {dt.datetime.now().day}일] 일본여행 정보'
message['From'] = privateKeys["sender_email"]
message['To'] = ",".join(recipients)
buttonStyle = """
  margin: 1rem 0 0 0;
  padding: 0.5rem 1rem;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 0.75rem;
  font-weight: 400;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  width: auto;
  color: white;
  background-color: #B1B2FF;

  border: none;
  border-radius: 4px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: 0.5s;
"""

def flightChangeMessage():
  if (yesterdayFlights - todayFlights > 0):
    return f"{(yesterdayFlights - todayFlights) // 3}건 감소한"
  elif (yesterdayFlights - todayFlights < 0):
    return f"{(todayFlights - yesterdayFlights) // 3}건 증가한"
  else:
    return "어제와 동일한"

content = f"""
    <html>
      <body>
          <p>어제 기준 비행 수 : {yesterdayFlights // 3}건</p>
          <p>오늘 기준 비행 수 : {flightChangeMessage()} {todayFlights // 3}건</p>
          <p>{df.iloc[length - 1]['date']} {df.iloc[length - 1]['time']} 기준 엔화 환율: <strong>{df.iloc[length -1]['currency']}</strong></p>
          <p>환율정보, 비행기표 별도 첨부</p>
          {flightTable}
          <p>위 표는 {dt.datetime.now()} 기준이며 몇 초 정도의 오차는 있을 수 있음</p>
          <a href={privateKeys["url"]} style="{buttonStyle}">지금 바로 보러가기&rarr;</a>
      </body>
    </html>
"""

def attach_image():
  filenames = ["price.png", "recent_currency.png"]
  try:
    for filename in filenames:
      fp = open(os.path.dirname(os.path.realpath(__file__)) + "/" + filename, 'rb')
      att = MIMEApplication(fp.read(), _subtype="pdf")
      fp.close()
      att.add_header('Content-Disposition', 'attachment', filename=filename)
      message.attach(att)
  except:
    print("no image file!")

def send_mail():
  attach_image()
  mimetext = MIMEText(content,'html')
  message.attach(mimetext)

  email_id = privateKeys["id"]
  email_pw = privateKeys["password"]

  server = smtplib.SMTP('smtp.naver.com',587)
  server.ehlo()
  server.starttls()
  server.login(email_id,email_pw)
  server.sendmail(message['From'],recipients,message.as_string())
  digit = "person" if len(recipients) == 1 else "people"
  print(f"✅ Mail sent to {len(recipients)} {digit}!")
  server.quit()

send_mail()