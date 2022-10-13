import flight

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import datetime as dt
import private
import os
import pandas as pd

df = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/" + "jpy_krw.csv", engine='python')
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

def attach_image(currency_code):
    filenames = ["price.png", f"recent_{currency_code.lower()}_currency.png"]
    try:
      for filename in filenames:
        fp = open(os.path.dirname(os.path.realpath(__file__)) + "/" + filename, 'rb')
        att = MIMEApplication(fp.read(), _subtype="pdf")
        fp.close()
        att.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(att)
    except:
      print("❌ no image file!")


def send_mail(mail, content, message, currency_code):
  attach_image(currency_code)
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
  today_flights, flight_table = flight.getFlightData(user["url"])
  recipient = user["mail"]
  message = MIMEMultipart()
  message['Subject'] = f'[{dt.datetime.now().month}월 {dt.datetime.now().day}일] {user["to_KOR"]} 여행 정보'
  message['From'] = private_keys["sender_email"]
  message['To'] = recipient

  content = f"""
      <html>
        <body>
            <h3>{user["departure"]} ~ {user["arrival"]}<br>{user["from_KOR"]}-{user["to_KOR"]} 왕복 비행정보</h3>
            <div>
              <p>오늘 비행 수 : {today_flights // 3}건</p>
            </div>
            <p>{df.iloc[df.shape[0] - 1]['date']} {df.iloc[df.shape[0] - 1]['time']} 기준 엔화 환율: <strong>{df.iloc[df.shape[0] -1]['currency']}</strong></p>
            <p>환율정보, 비행기표 별도 첨부</p>
            {flight_table}
            <p>위 표는 {dt.datetime.now()}에 작성됨</p>
            <p>환율은 오전 09:00 시작가 기준</p>
            <a href={user["url"]} style="{buttonStyle}">지금 바로 보러가기&rarr;</a>
        </body>
      </html>
  """
  try:
    send_mail(recipient, content, message, user["currency_code"])
  except:
    print("❌ Error occured while sending mail...")