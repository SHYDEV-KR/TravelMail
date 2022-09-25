import flight
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime as dt
import private
import os


privateKeys = private.myKeys()
flightTable = flight.getFlightData(privateKeys["url"])

def formatDateToKorean():
  today = dt.datetime.now()
  return f"{today.month}월 {today.day}일"

recipients = privateKeys["recipients"]

title = f"[{formatDateToKorean()}] 후쿠오카 왕복 최저가"

message = MIMEMultipart()
message['Subject'] = title
message['From'] = privateKeys["sender_email"]
message['To'] = ",".join(recipients)

filename = "price.png"
try:
  fp = open(os.path.dirname(os.path.realpath(__file__)) + "/" + filename, 'rb')
  att = MIMEApplication(fp.read(), _subtype="pdf")
  fp.close()
  att.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(att)
except:
  print("no image file!")

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

content = f"""
    <html>
      <body>
          <h3>{title}</h3>
          <p>마음을 담아 보내드립니다 *^^*</p>
          <p>사진도 참고하세요 ㅎㅎ</p>
          {flightTable}
          <p>위 표는 {dt.datetime.now()} 기준이며 몇 초 정도의 오차는 있을 수 있음</p>
          <a href={privateKeys["url"]} style="{buttonStyle}">지금 바로 보러가기&rarr;</a>
      </body>
    </html>
"""

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