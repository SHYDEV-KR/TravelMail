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
currency_visualization.generate_image()
private_keys = private.my_keys()
user_data = private.user_data()

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

def flight_change_msg(yesterday_flights, today_flights):
  today_flights = today_flights // 3
  if (yesterday_flights - today_flights > 0):
    return f"{(yesterday_flights - today_flights)}건 감소한"
  elif (yesterday_flights - today_flights < 0):
    return f"{(today_flights - yesterday_flights)}건 증가한"
  else:
    return "어제와 동일한"


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


def send_mail(mail, content, message):
  attach_image()
  mimetext = MIMEText(content,'html')
  message.attach(mimetext)

  email_id = private_keys["id"]
  email_pw = private_keys["password"]

  server = smtplib.SMTP('smtp.naver.com',587)
  server.ehlo()
  server.starttls()
  server.login(email_id,email_pw)
  server.sendmail(message['From'],mail,message.as_string())
  print(f"✅ Mail sent to {mail}!")
  server.quit()


for user in user_data:
  yesterday_flights = user["yesterday_flights"]
  today_flights, flight_table = flight.getFlightData(user["url"])
  recipient = user["mail"]
  message = MIMEMultipart()
  message['Subject'] = f'[{dt.datetime.now().month}월 {dt.datetime.now().day}일] {user["to_KOR"]} 여행 정보'
  message['From'] = private_keys["sender_email"]
  message['To'] = recipient

  content = f"""
      <html>
        <body>
            <h3>{user["departure"]} ~ {user["arrival"]} {user["from_KOR"]}-{user["to_KOR"]} 왕복 비행정보</h3>
            <div>
              <p>어제 기준 비행 수 : {yesterday_flights}건</p>
              <p>오늘 기준 비행 수 : {flight_change_msg(yesterday_flights, today_flights)} {today_flights // 3}건</p>
            </div>
            <p>{df.iloc[df.shape[0] - 1]['date']} {df.iloc[df.shape[0] - 1]['time']} 기준 엔화 환율: <strong>{df.iloc[df.shape[0] -1]['currency']}</strong></p>
            <p>환율정보, 비행기표 별도 첨부</p>
            {flight_table}
            <p>위 표는 {dt.datetime.now()} 기준이며 몇 초 정도의 오차는 있을 수 있음</p>
            <a href={private_keys["url"]} style="{buttonStyle}">지금 바로 보러가기&rarr;</a>
        </body>
      </html>
  """
  try:
    send_mail(recipient, content, message)
  except:
    print("❌ Error occured while sending mail...")