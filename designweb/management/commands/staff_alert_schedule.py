__author__ = 'zys'
from django.core.management.base import BaseCommand, CommandError
from designweb.emailer.email_utils import *
from designweb.utils import sending_order_confirmation_email
from designweb.models import Order


class Command(BaseCommand):
    args = '< email_address email_address ...>'
    help = 'please enter email addresses'

    def handle(self, *args, **options):
        signup_email = Email()
        order_list = Order.get_unconfirmed_orders()
        email_list = []

        for email_address in args:
            try:
                email_list.append(email_address)
            except:
                raise CommandError('the email "%s" does not exist' % email_address)

        for order in order_list:
            sending_order_confirmation_email(order.user, order)
            template_dict = {
                'username': order.user.username,
                'user_id': order.user.pk,
                'order_id': order.pk,
                'subtotal': order.subtotal,
                'payment_resource': order.payment_resource,
                'payment_transaction_id': order.payment_transaction_id,
                'modified_date': order.modified_date,
            }
            signup_email.send_email({CONSTANT_DICT_FIELD_SUBJECT: '1dots [STAFF] : Sales Alert ',
                                    CONSTANT_DICT_FIELD_TO_LIST: email_list,
                                    CONSTANT_DICT_FIELD_TEMPLATE_TYPE: MAIL_TYPE_STAFF_ALERT,
                                    CONSTANT_DICT_FIELD_TEMPLATE_CONTENT: template_dict, })
            order.is_alert = True
            order.save()
        signup_email.close_connection()
