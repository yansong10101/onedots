from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta, time
from designweb.shipping.shipping_utils import shipping_fee_multi_calc
from designweb.payment.tax_utils import get_tax_combine_rate_by_zip


# User profile
class UserProfile(models.Model):
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, primary_key=True, related_name='user_profile')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default='', blank=True)
    is_designer = models.BooleanField(default=False, blank=True)
    designer_type = models.CharField(max_length=50, blank=True)
    address1 = models.CharField(max_length=50, blank=True)
    address2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip = models.CharField(max_length=8, blank=True)
    phone1 = models.CharField(max_length=15, blank=True)
    phone2 = models.CharField(max_length=15, blank=True)

    def raw_data(self):
        return {
            'user': self.user.id,
        }

    def has_address_info(self):
        # implement for detecting if this user has full address info for shipping
        pass

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Category(models.Model):
    PARENT_CAT_CHOICE = (
        ('Color', 'Color'),
        ('Category', 'Category'),
        ('Fashion', 'Fashion'),
    )
    category_name = models.CharField(max_length=25)
    parent_category = models.CharField(max_length=25, choices=PARENT_CAT_CHOICE, blank=True)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    # the highest is 0
    PRIOR_LEVEL = (
        (0, 'high'),
        (1, 'middle'),
        (2, 'low',),
    )
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=20, unique=True, editable=False)
    price = models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True)  # if null show 'please call' msg
    designer = models.ForeignKey(User, related_name='products', null=True)
    category = models.ManyToManyField(Category, blank=True, related_name='products')
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    image_root = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_customize = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    number_in_stock = models.IntegerField(default=0)
    shipping_msg = models.CharField(max_length=100, blank=True)
    important_msg = models.CharField(max_length=100, blank=True)
    group_duration = models.IntegerField(default=4)
    group_discount = models.DecimalField(decimal_places=3, max_digits=4, default=1.00)  # ex, 10% off : 0.90
    general_discount = models.DecimalField(decimal_places=3, max_digits=4, default=1.00)
    number_like = models.IntegerField(default=0)
    average_review_score = models.DecimalField(default=5, decimal_places=1, max_digits=2)
    prior_level = models.IntegerField(choices=PRIOR_LEVEL, default=2)
    manually_set_prior_level = models.IntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
            call twice save():
                first time to get pk value from database calculation
                second save() just use to update product_code value
        """
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        current_year = str(date.today().year)
        code_number = str(self.pk).zfill(7)
        self.product_code = current_year + code_number
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.product_name


class CustomerReview(models.Model):
    product = models.ForeignKey(Product, related_name='product_review')
    customer = models.ForeignKey(User, related_name='reviewed_customer')
    total_number = models.IntegerField(default=0)
    review_score = models.DecimalField(default=5, decimal_places=1, max_digits=2)
    message = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.product.product_name


class ProductComment(models.Model):
    product = models.ForeignKey(Product, related_name='product_forum')
    reviewer = models.CharField(max_length=50, default='stranger')
    reviewer_id = models.IntegerField(default=0)
    message = models.TextField(blank=True, max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    photo_img = models.CharField(max_length=25, default='/stranger')

    def __str__(self):
        return self.product.product_name


class ProductExtension(models.Model):
    product = models.OneToOneField(Product, related_name='details', primary_key=True)
    price_range = models.DecimalField(decimal_places=2, default=0.00, max_digits=8)
    special_price = models.DecimalField(decimal_places=2, default=0.00, max_digits=8)
    message = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    feature = models.TextField(blank=True)
    # product attributes
    size = models.CharField(max_length=225, blank=True)
    weight = models.CharField(max_length=20, blank=True, default='1.00')
    color = models.CharField(max_length=150, blank=True)             # format example: blue|white|red|green

    def __str__(self):
        return self.product.product_name


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    total_items = models.IntegerField(blank=True, default=1)
    is_paid = models.BooleanField(default=False)
    payment_transaction_id = models.CharField(max_length=50, blank=True)
    payment_resource = models.CharField(max_length=50, blank=True)
    payment_status = models.CharField(max_length=10, blank=True, default='NotPaid')     # Approval, Pending, Cancel...
    payment_method = models.CharField(max_length=15, blank=True)
    total_amount = models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True)
    total_tax = models.DecimalField(decimal_places=2, default=0.00, max_digits=7)
    total_shipping = models.DecimalField(decimal_places=2, default=0.00, max_digits=7)
    total_discount = models.DecimalField(decimal_places=2, default=0.00, max_digits=7)
    subtotal = models.DecimalField(decimal_places=2, default=0.00, max_digits=7)

    receiver_first_name = models.CharField(max_length=25, default='')
    receiver_last_name = models.CharField(max_length=25, default='')
    billing_first_name = models.CharField(max_length=25, default='')
    billing_last_name = models.CharField(max_length=25, default='')
    shipping_address1 = models.CharField(max_length=50, blank=True)
    shipping_address2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=20, blank=True)
    shipping_state = models.CharField(max_length=2, blank=True)
    shipping_zip = models.CharField(max_length=8, blank=True)
    shipping_phone1 = models.CharField(max_length=15, blank=True)
    shipping_phone2 = models.CharField(max_length=15, blank=True)
    billing_address1 = models.CharField(max_length=50, blank=True)
    billing_address2 = models.CharField(max_length=50, blank=True)
    billing_city = models.CharField(max_length=20, blank=True)
    billing_state = models.CharField(max_length=2, blank=True)
    billing_zip = models.CharField(max_length=8, blank=True)
    billing_phone1 = models.CharField(max_length=15, blank=True)
    billing_phone2 = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username

    def get_total_payment(self):
        order_detail_list = self.details.all()
        shipping_cost_list = []
        items_subtotal = 0.00
        for detail in order_detail_list:
            prod_name = detail.product.product_name
            prod_price = float(detail.product.price)
            prod_weight = float(detail.product.details.weight)
            num_items = int(detail.number_items)
            items_subtotal += prod_price * num_items
            shipping_cost_list.append({
                'name': prod_name,
                'weight': prod_weight,
                'total': num_items,
            })
        shipping_fee = shipping_fee_multi_calc(shipping_cost_list)
        tax = 0.00
        if self.billing_zip:
            tax_rate = float('{0:.2f}'.format(float(get_tax_combine_rate_by_zip(self.billing_zip))))
            tax = float('{0:.2f}'.format(tax_rate * items_subtotal))
        discount = 0.00
        # make currency amount
        items_subtotal = float('{0:.2f}'.format(items_subtotal))
        discount = float('{0:.2f}'.format(discount))
        subtotal = float('{0:.2f}'.format(items_subtotal + shipping_fee + tax - discount))
        if subtotal < 0.00:
            return None
        return {'items_subtotal': items_subtotal,
                'shipping_fee': shipping_fee,
                'tax': tax,
                'discount': discount,
                'subtotal': subtotal}

    def save_payments_info(self):
        payment_dict = self.get_total_payment()
        if payment_dict:
            self.total_amount = payment_dict['items_subtotal']
            self.total_discount = payment_dict['discount']
            self.total_shipping = payment_dict['shipping_fee']
            self.total_tax = payment_dict['tax']
            self.subtotal = payment_dict['subtotal']
            self.save()

    def update_order_details_product_count(self, prod_id, num_items):
        for order_detail in self.details.all():
            if order_detail.product.pk == prod_id:
                order_detail.number_items = num_items
                order_detail.save()


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='details', editable=False)
    product = models.ForeignKey(Product, related_name='products', editable=False)  # , unique=True
    number_items = models.IntegerField(default=1, blank=True, editable=False)
    subtotal = models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True)
    shipping_costs = models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True)
    tax = models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True)
    shipping_company = models.CharField(max_length=50, blank=True)
    shipping_status = models.CharField(max_length=1, blank=True)
    tracking_code = models.CharField(max_length=50, blank=True)
    shipping_date = models.DateTimeField(blank=True, null=True)
    receive_date = models.DateTimeField(blank=True, null=True)
    size = models.CharField(max_length=50, default='')
    weight = models.CharField(max_length=20, blank=True, default='1.00')
    color = models.CharField(max_length=25, default='')

    def get_order_id(self):
        return self.order.pk
    get_order_id.short_description = 'Order ID'

    def is_order_paid(self):
        return self.order.is_paid
    is_order_paid.short_description = 'Payment Status'

    def is_tracking_code_filled(self):
        return bool(self.tracking_code)
    is_tracking_code_filled.short_description = 'tracking Code Status'

    def __str__(self):
        return str(self.order.user.username)


class WishList(models.Model):
    user = models.OneToOneField(User, related_name='wish_list', primary_key=True)
    products = models.ManyToManyField(Product, related_name='wish_lists', blank=True)
    number_items = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', primary_key=True)
    products = models.ManyToManyField(Product, related_name='carts', blank=True)
    number_items = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class CartDetail(models.Model):
    STATUS_OPTION = (
        ('Active', 'Active'),
        ('Deleted', 'Deleted'),
    )
    cart = models.ForeignKey(Cart, related_name='cart_details')
    product = models.ForeignKey(Product, related_name='product')
    number_in_cart = models.IntegerField(default=1)
    status = models.CharField(max_length=15, choices=STATUS_OPTION, blank=True)
    size = models.CharField(max_length=50, default='')
    weight = models.CharField(max_length=20, blank=True, default='1.00')
    color = models.CharField(max_length=25, default='')

    def __str__(self):
        return self.cart.user.username


class MicroGroup(models.Model):
    members = models.ManyToManyField(User, related_name='micro_groups')
    product = models.ForeignKey(Product, related_name='micro_groups')
    owner = models.ForeignKey(User, related_name='micro_group')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    duration_time = models.IntegerField(default=4)
    group_price = models.DecimalField(decimal_places=2, blank=True, max_digits=7, null=True)
    group_discount = models.DecimalField(decimal_places=3, blank=True, max_digits=4, default=1.00)
    activate_line = models.IntegerField(default=4)

    def __str__(self):
        return self.owner.username + '-' + self.product.product_name

    def get_remain_time(self):
        time_now = datetime.now()
        end_time = self.created_date.replace(tzinfo=None) + timedelta(hours=self.duration_time)
        remain_time = end_time - time_now
        if remain_time.days < 0:
            return time(hour=0, minute=0, second=0)
        seconds = remain_time.seconds
        hour = seconds // 3600
        minute = (seconds % 3600) // 60
        second = (seconds % 60)
        remain_time = time(hour=hour, minute=minute, second=second)
        return remain_time

    def get_remain_time_by_seconds(self):
        time_now = datetime.now()
        end_time = self.created_date.replace(tzinfo=None) + timedelta(hours=self.duration_time)
        remain_time = end_time - time_now
        if remain_time.days < 0:
            return 0
        return remain_time.seconds

    def get_end_time(self):
        return self.created_date.replace(tzinfo=None) + timedelta(hours=self.duration_time)


class GroupDetails(models.Model):
    group = models.ForeignKey(MicroGroup, related_name='group_detail')
    member = models.ForeignKey(User, related_name='group_detail')
    join_date = models.DateTimeField(auto_now_add=True, editable=False)
    email = models.CharField(max_length=70)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.group
