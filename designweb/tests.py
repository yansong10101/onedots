# from django.test import TestCase
# from designweb import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from hookupdesign.settings import EMAIL_HOST_USER
from designweb.payment.payment_utils import *


# Create your tests here.
def db_read():
    user = User.get_full_name(User.objects.filter(username='yansong').first())
    return str(user)


def create_user():
    User.objects.create_user('testOne', email='test@gmail.com', password='testOne')


def mail_test():
    send_mail('Subject here',
              'Here is the message.',
              EMAIL_HOST_USER,
              ['yansong10101@gmail.com'],
              fail_silently=False)


def scheduler_test():
    pass


def test_memcachier():
    from django.core.cache import cache
    c_list = ['item one', 'item two', 'item three', 'item four']
    cache.set('list', c_list)
    print(cache.get('list'))
    for item in cache.get('list'):
        print(item)

    c_dict = {'key 1': 'item 1', 'key 2': 'item 2',
              'key 3': {
                  'inner key': 'inner value',
                  'inner test': 'testing'
              }}
    cache.set('dict', c_dict)
    print(cache.get('dict'))

    print(cache.get('dict')['key 1'])
    print(cache.get('dict')['key 3']['inner key'])

    cache.delete('dict')

    print(cache.get('dict'))


def test_memcachier_2():
    from django.core.cache import cache
    cache.set('index', [1, 2, 3, 4])
    c_list = cache.get('index')
    c_list[0] = c_list[0] + 10
    print(c_list)


def check_image_list(image_list):
    big_list = []
    small_list = []
    for big_image in image_list:
        big_tokens = (str(big_image).split('.')[0]).split('_')
        if big_tokens[0] == 'b':
            for small_image in image_list:
                small_tokens = (str(small_image).split('.')[0]).split('_')
                if small_tokens[0] == 's' and big_tokens[2] == small_tokens[2]:
                    big_list.append(big_image)
                    small_list.append(small_image)
                    break
    return {'big_img': big_list, 'small_img': small_list}


def test_s3_bucket(product_code):
    from hookupdesign import settings
    from boto.s3.connection import S3Connection
    import mimetypes
    import re
    conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    product_dir = 'test/static/products/' + str(product_code) + '/'
    rs = bucket.list(prefix=product_dir)
    image_list = []
    for item in rs:
        bucket_key = item.name
        if mimetypes.guess_type(bucket_key)[0]:  # check if is image file extension, assume only image or none
            print(bucket_key)
            image_list.append(re.sub(product_dir, '', bucket_key))
    print(check_image_list(image_list))


def test_payment(payment_method, host_root, transaction_object, card_info={}):

    if payment_method == PAYPAL:
        card_info = {}
    elif payment_method == DIRECT_CREDIT:
        pass

    print(transaction_object)
    print(card_info)

    auth_payment()
    payment = Payment(get_payment_json(payment_method, host_root, transaction_object, card_info))
    is_approve = payment.create()

    print(is_approve)

    payment_dict = {'payment_id': payment.id, 'payment_state': payment.state, 'redirect_url': None}

    if is_approve:
        print("Payment[%s] created successfully" % payment.id)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % redirect_url)
                payment_dict['redirect_url'] = redirect_url
                return payment_dict
    else:
        print('payment cannot be approval, please check your payment info ...')
        return None
    print("Direct credit -- Payment[%s] execute successfully" % (payment.id))
    # for direct_credit return
    return payment_dict