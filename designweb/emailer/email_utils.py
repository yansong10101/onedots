__author__ = 'zys'
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hookupdesign.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from string import Template
from designweb.emailer import MAIL_TYPE_WELCOME, MAIL_TYPE_SUMMERY, MAIL_TYPE_STAFF_ALERT, \
    WELCOME_EMAIL_TEMPLATE, PAYMENT_SUCCESS_SUMMERY, STAFF_ORDER_PAYMENT_ALERT, CONSTANT_DICT_FIELD_SUBJECT, \
    CONSTANT_DICT_FIELD_FROM, CONSTANT_DICT_FIELD_TO, CONSTANT_DICT_FIELD_TEMPLATE_TYPE, \
    CONSTANT_DICT_FIELD_TEMPLATE_CONTENT, CONSTANT_DICT_FIELD_TO_LIST


class Email:
    """
    Initial mail template and send to single or multiple users by email.
    email generator will check email type and use the right template.
    Please see private method : set_mail_template()
    """
    message = MIMEMultipart()

    def __init__(self):
        self.mail_server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        self.mail_server.ehlo()
        self.mail_server.starttls()
        self.mail_server.ehlo()
        self.mail_server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    def start_connection(self):
        self.mail_server.connect(host=EMAIL_HOST, port=EMAIL_PORT)

    def close_connection(self):
        self.mail_server.quit()

    def send_email(self, mail_content_dict):
        """
        :param
            username -- (email address);
            mail_content_dict contains :
                Subject,
                From (option, default from hello@1dots.com),
                To (email to list),
                template_type,
                template_content
        """
        email_to_list = mail_content_dict[CONSTANT_DICT_FIELD_TO_LIST]
        for email_to in email_to_list:
            self.set_mail_template(email_to, mail_content_dict)
            self.mail_server.sendmail(EMAIL_HOST_USER, email_to, self.message.as_string())
        self.message = MIMEMultipart()
        # self.close_connection()

    def set_mail_template(self, email_to, mail_content_dict):
        self.message[CONSTANT_DICT_FIELD_SUBJECT] = mail_content_dict[CONSTANT_DICT_FIELD_SUBJECT]
        self.message[CONSTANT_DICT_FIELD_FROM] = EMAIL_HOST_USER
        self.message[CONSTANT_DICT_FIELD_TO] = email_to
        template_type = mail_content_dict[CONSTANT_DICT_FIELD_TEMPLATE_TYPE]
        template_content = mail_content_dict[CONSTANT_DICT_FIELD_TEMPLATE_CONTENT]
        part = None
        if template_type == MAIL_TYPE_WELCOME:
            part = Email.template_substitution_generator(WELCOME_EMAIL_TEMPLATE, template_content)
        if template_type == MAIL_TYPE_SUMMERY:
            part = Email.template_substitution_generator(PAYMENT_SUCCESS_SUMMERY, template_content)
        if template_type == MAIL_TYPE_STAFF_ALERT:
            part = Email.template_substitution_generator(STAFF_ORDER_PAYMENT_ALERT, template_content)
        self.message.attach(MIMEText(part, 'html'))

    @staticmethod
    def template_substitution_generator(template, sub_dict):
        """
        :param template:
        :param sub_dict:
        :return: template after substitution key words by passed in dict,
            MUST HAVE :
            1. Welcome email template:
                No need
            2. Staff alert template:
                $username, $user_id, $order_id, $subtotal, $payment_resource, $payment_transaction_id, $modified_date
            3. order summery for customer
                ... TBD ...
        """
        if sub_dict:
            return Template(template).substitute(sub_dict)
        return template
