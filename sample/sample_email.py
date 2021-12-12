import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.sina.com"
PORT = 25
FROM_USER = "aa@sina.com"
PASSWD = "密码或者授权码"

msg = EmailMessage()
msg["From"] = FROM_USER
msg["To"] = ", ".join(["bb@qq.com"])
msg["Subject"] = "Simple Test"
msg.set_content("this is a email content")

with smtplib.SMTP(host=SMTP_SERVER, port=PORT) as client:
    client.set_debuglevel(1)
    client.login(FROM_USER, PASSWD)
    client.send_message(msg)
