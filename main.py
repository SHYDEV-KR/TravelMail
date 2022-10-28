import time
import datetime as dt
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import flight
import private.private as private
import db
from currency import get_latest_currency

private_keys = private.my_keys()
order_queries = db.get_queries_from_database(private_keys["db_id"])

buttonStyle = """
  margin: 1rem 0 0 0; padding: 0.5rem 1rem; font-family: 'Noto Sans KR', sans-serif;
  font-size: 0.75rem; font-weight: 400; text-align: center; text-decoration: none; display: inline-block;
  width: auto; color: white; background-color: #B1B2FF; border: none; border-radius: 4px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  cursor: pointer; transition: 0.5s;
"""

def attach_image(currency_code):
    filenames = ["price.png", f"recent_{currency_code.lower()}_currency.png"]
    try:
      for filename in filenames:
        fp = open(os.path.dirname(os.path.realpath(__file__)) + "/img/" + filename, 'rb')
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
  print(f"📮 Mail sent to {mail}!", end=" ")
  server.quit()


for query in order_queries:
  start_user = time.time()
  order = db.get_order_data_from_single_query(query)
  today_flights, table_rows, flight_table = flight.get_flight_data(order["url"])
  latest_currency = get_latest_currency(order["currency_code"])
  recipient = order["users"]
  message = MIMEMultipart()
  message['Subject'] = f'[{dt.datetime.now().month}월 {dt.datetime.now().day}일] {order["arrival_city"]["name"]} 여행 정보'
  message['From'] = private_keys["sender_email"]

  content = f"""
      <html>
        <body>
            <h3>{order["departure_date"]} ~ {order["arrival_date"]}<br>{order["departure_city"]["name"]}-{order["arrival_city"]["name"]} 왕복 비행정보</h3>
            <div>
              <p>오늘 비행 수 : {today_flights}건</p>
            </div>
            <p>{latest_currency['date']} {order["currency_code"]} 환율: <strong>{latest_currency['currency']}</strong></p>
            <p>**최저가 {table_rows}개만 표시, 환율정보, 비행기표 별도 사진 첨부</p>
            {flight_table}
            <p>위 표는 {dt.datetime.now()}에 작성됨</p>
            <p>환율은 오전 09:00 시작가 기준</p>
            <a href={order["url"]} style="{buttonStyle}">지금 바로 보러가기&rarr;</a>
        </body>
      </html>
  """
  try:
    send_mail(recipient, content, message, order["currency_code"])
    print(f"(took {round(time.time() - start_user, 3)}s)")
    print()
  except:
    print("❌ Error occured while sending mail...")