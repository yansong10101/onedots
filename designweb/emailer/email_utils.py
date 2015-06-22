__author__ = 'zys'
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hookupdesign.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


MAIL_TYPE_WELCOME = 'welcome'
MAIL_TYPE_SUMMERY = 'summery'
WELCOME_EMAIL_TEMPLATE = """
    <html>
      <head></head>
      <body>
        <p>Hello!</p>
        <p>Welcome to 1dots !</p>
        <p>You will discover and buy amazing, creative design things !</p>
        <p>Confirm you email address and to make sure you receive important notifications</p>
      </body>
    </html>
"""
PAYMENT_SUCCESS_SUMMERY = """
    <html>
      <head></head>
      <body>
        <p>shipping address:</p>
        <p>{{shipping_info.first_name}} {{shipping_info.last_name}}</p>
        <p>{{shipping_info.address_1}} {{shipping_info.address_2}}</p>
        <p>{{shipping_info.city}}, {{shipping_info.state}} {{shipping_info.zip}}</p>
      </body>
    </html>
"""


class Email:
    message = MIMEMultipart()

    def __init__(self):
        self.mail_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        self.mail_server.ehlo()
        self.mail_server.starttls()
        self.mail_server.ehlo()
        self.mail_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    def start_connection(self):
        self.mail_server.connect(host=EMAIL_HOST, port=EMAIL_PORT)

    def send_email(self, email_to):
        self.mail_server.sendmail(EMAIL_HOST_USER, email_to, self.message.as_string())

    def close_connection(self):
        self.mail_server.quit()

    def set_mail_template(self, mail_content_dict):
        self.message['Subject'] = mail_content_dict['Subject']
        self.message['From'] = EMAIL_HOST_USER
        self.message['To'] = mail_content_dict['To']

        part = MIMEText(WELCOME_EMAIL_TEMPLATE, 'html')
        if mail_content_dict['template_type'] == MAIL_TYPE_SUMMERY:
            part = MIMEText(PAYMENT_SUCCESS_SUMMERY, 'html')
        self.message.attach(part)
