import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import date
from email.utils import formataddr

load_dotenv()

def send(email, email_subject, headline, image, articles, rumors, bets, includeBets):
    print('bets', bets)
    print(type(bets))
    server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    server.login(user=os.getenv('SMTP_USER'),password=os.getenv('SMTP_PASSWORD'))

    env = Environment(
        loader=PackageLoader("server"),
        autoescape=select_autoescape()
    )
    template = env.get_template("template.html")
    
    today = date.today()
    today.strftime("%A, %B %d, %Y")
    html = template.render(headline=headline, image=image, articles=articles, rumors=rumors, bets=bets, includeBets=includeBets, today=today)

    message = MIMEMultipart("alternative")
    message["Subject"] = email_subject
    message['From'] = formataddr(('Dribble Digest', 'dribbledigest1@gmail.com'))
    message["To"] = email

    message.attach(MIMEText(html, "html"))

    server.sendmail(from_addr='dribbledigest1@gmail.com', to_addrs=[email], msg=message.as_string())
