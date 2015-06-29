__author__ = 'zys'

MAIL_TYPE_WELCOME = 'welcome'
MAIL_TYPE_SUMMERY = 'summery'
MAIL_TYPE_STAFF_ALERT = 'staff_alert'
WELCOME_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">
<title></title>
</head>
<body style="width: 800px; padding: 10px 50px;">
<div style="text-align: center;">
<img src="https://s3-us-west-1.amazonaws.com/popdesign/static/email_template/welcome_email_temp.jpg"
style="height: 400px;">
</div>
<div style="text-align: left; margin-left: 80px;">
<h3>Hello $username!</h3>
<p>Welcome to 1dots !</p>
<p>You will discover and buy amazing, creative design things !</p>
<p>Confirm you email address and to make sure you receive important notifications</p>
</div>
</body>
</html>
"""
PAYMENT_SUCCESS_SUMMERY = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">
<title></title>
</head>
<body style="width: 800px; padding: 10px 50px;">

<style>
p {margin-bottom: 0px; margin-top: 0px;}
</style>
<div style="text-align: center;">
<img src="https://s3-us-west-1.amazonaws.com/popdesign/static/email_template/welcome_email_temp.jpg"
style="height: 400px;">
<h3 style="float: left; margin-left: 80px;">Hello $username</h3>
<h3 style="float: right; margin-right: 80px;">Order Confirmation : $order_id</h3>
</div>
<div style="width: 40%; float: right; margin-top: 56px; margin-right: 80px;">
<p>Order details : </p>
<ul  style="padding-left: 15px;">
<p>number items : $order_number_items</p>
<p>order date : $order_date</p>
<p>total amount : $order_total_amount</p>
<p>shipping fee : $order_shipping_cost</p>
<p>discount : $order_discount</p>
<p>tax : $order_tax</p>
<p>subtotal : $order_subtotal</p>
</ul>
</div>
<div style="margin-top: 80px; width: 40%; margin-left: 80px">
<p style="margin-bottom: 20px;">Thank you for shopping with us !</p>
<div style="width: 50%;">
<p>shipping info:</p>
<ul style="padding-left: 15px;">
<p>$shipping_name</p>
<p>$shipping_address_1, $shipping_address_2</p>
<p>$shipping_city, $shipping_state $shipping_zip</p>
</ul>
</div>
</div>
<div style="text-align: right; margin-right: 80px; margin-top: 50px;">
<p>Contact us by email : hello@1dots.com</p>
</div>
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
