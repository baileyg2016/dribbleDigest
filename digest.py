import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def send_digest(email):
    server = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    server.login(user=os.getenv('SMTP_USER'),password=os.getenv('SMTP_PASSWORD'))

    html = """\
<html>
   <body>
    <div style="max-width: 670px; background-color: #060B1C; font-family: &quot;Inter&quot;, BlinkMacSystemFont, -apple-system, &quot;Segoe UI&quot;, &quot;Roboto&quot;, &quot;Oxygen&quot;, &quot;Ubuntu&quot;, &quot;Cantarell&quot;, &quot;Fira Sans&quot;, &quot;Droid Sans&quot;, &quot;Helvetica Neue&quot;, &quot;Helvetica&quot;, &quot;Arial&quot;, sans-serif !important;">
           <table style="width: 100%;">
               <tr>
                   <td style="text-align: center;">
                       <img style="width: 12rem; height: auto; margin-top: 6rem;" src="https://hackstoragedribbledigest.blob.core.windows.net/svgs/dribbledigest.svg" alt="Logo">
                   </td>
               </tr>
           </table>

           <!-- TODO headline link -->
           <a href="https://example.com" style="color: #fff; font-size: 2rem; font-weight: 800; text-align: center; display: block; text-decoration: none; margin: 4rem 4rem 0 4rem;">
               <!-- TODO headline -->
               "Josh Jacobs Rumors: Dolphins Inquired About Trade, Raiders Said RB Isn't Available"
           </a>

           <table style="width: 100%;">
               <tr>
                   <td style="text-align: center;">
                      <div style="display: inline-block; width: 35px; height: 2px; background-color: #fff; border-radius: 10px; margin: 1rem 0 1rem 0;">

                      </div>
                   </td>
               </tr>
           </table>

           <p style="color: #B4B6BB; font-size: .8rem; font-weight: 400; text-align: center; margin: 0;">
               <!-- TODO date -->
               Friday, August 25, 2023
           </p>

           <div style="margin: 4rem 4.5rem 0 4.5rem">
               <img style="width: 100%; height: auto; border-radius: 10px;" src="https://media.bleacherreport.com/image/upload/w_800,h_533,c_fill/v1692882843/tooaszoxs90ozmja1yvh.jpg" alt="Headline image">
           </div>

           <table style="width: 100%;">
               <tr>
                   <td style="width: 4rem;"></td>
                   <td>
                       <p style="color: #fff; font-size: 2rem; font-weight: 800; text-align: center; display: block; text-decoration: none; margin: 2rem 4rem 0 4rem;">
                           Betting Lines
                       </p>

                       <div style="height: 10rem;"></div>
                   </td>
                   <td style="width: 4rem;"></td>
               </tr>
           </table>
       </div>
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
    send_digest('baileyg2016@gmail.com')

if __name__ == "__main__":
    main()