__author__ = 'zys'
from django.core.management.base import BaseCommand
from designweb.utils import sending_order_confirmation_email
from designweb.models import Order


class Command(BaseCommand):
    args = '< email_address email_address ...>'
    help = 'please enter email addresses'

    def handle(self, *args, **options):
        order_list = Order.get_unconfirmed_orders()
        for order in order_list:
            sending_order_confirmation_email(order.user, order)
