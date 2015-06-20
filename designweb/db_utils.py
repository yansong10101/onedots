__author__ = 'zys'
from designweb.models import *
from django.shortcuts import get_object_or_404
from django.core.exceptions import *

DB_FIELD_STATUS = 'payment_status'
DB_FIELD_IS_PAID = 'is_paid'


def delete_all_items_from_cart(cart):
    try:
        CartDetail.objects.filter(cart=cart).delete()
        cart.products.remove()
    except ObjectDoesNotExist:
        return


def mark_all_items_from_order(order, payment_dict):
    order.is_paid = True
    order.payment_status = 'Paid'
    order.payment_method = 'payment_method'
    order.payment_transaction_id = payment_dict['payment_id']
    order.total_amount = float(payment_dict['items_subtotal'])
    order.subtotal = float(payment_dict['subtotal'])
    order.total_tax = float(payment_dict['tax'])
    order.total_shipping = float(payment_dict['shipping_fee'])
    order.total_discount = float(payment_dict['discount'])
    order.save()


def update_all_cart_order_after_paid(user, order_id, payment_dict):
    cart = get_object_or_404(Cart, user=user)
    order = get_object_or_404(Order, pk=order_id)
    delete_all_items_from_cart(cart)
    mark_all_items_from_order(order, payment_dict)
