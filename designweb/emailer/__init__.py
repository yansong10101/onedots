__author__ = 'zys'

MAIL_TYPE_WELCOME = 'welcome'
MAIL_TYPE_SUMMERY = 'summery'
MAIL_TYPE_STAFF_ALERT = 'staff_alert'
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
        <p>$first_name $last_name</p>
        <p>$address_1, $address_2</p>
        <p>$city, $state, $zip</p>
      </body>
    </html>
"""
STAFF_ORDER_PAYMENT_ALERT = """
    <html>
      <head></head>
      <body>
        <h2>Payment Alert</h2>
        <p>Date -- $modified_date</p>
        <p>user name -- $username</p>
        <p>user id -- $user_id</p>
        <p>order id -- $order_id</p>
        <p>total paid -- $subtotal</p>
        <p>payment id -- $payment_resource</p>
        <p>transaction id -- $payment_transaction_id</p>
      </body>
    </html>
"""

# email dict content constant vars
CONSTANT_DICT_FIELD_SUBJECT = 'Subject'
CONSTANT_DICT_FIELD_FROM = 'From'
CONSTANT_DICT_FIELD_TO = 'To'
CONSTANT_DICT_FIELD_TO_LIST = 'email_to_list'
CONSTANT_DICT_FIELD_TEMPLATE_TYPE = 'template_type'
CONSTANT_DICT_FIELD_TEMPLATE_CONTENT = 'template_content'
