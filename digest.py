import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_digest(email):
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(host='smtp.gmail.com', post=465, context=context)
    server.login(user=os.getenv('SMTP_USER'),password=os.getenv('SMTP_PASSWORD'))

    html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

    message = MIMEMultipart("alternative")
    message["Subject"] = "Today's Digest"
    message["From"] = 'dribbledigest1@gmail.com'
    message["To"] = email

    message.attach(MIMEText(html, "html"))

    server.sendmail(from_addr='dribbledigest1@gmail.com', to_addrs=[email], msg=message.as_string())

def main():
    send_digest('extraneousprofiles@gmail.com')

if __name__ == "__main__":
    main()