from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.forms import UserCreationForm
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from designweb.serializer import *
from designweb.forms import *
from designweb.utils import *
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import json
from designweb.caches.group_utils import *
from designweb.payment.payment_utils import payment_process, DIRECT_CREDIT


def home(request):
    return render(request, 'home.html', get_display_dict(title='HOME'))


def index(request):
    # print(request.session)
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         return render(request, 'home.html', {'title': form.cleaned_data['username']})
    #     else:
    #         print(form.cleaned_data['error'])
    # else:
    #     form = LoginForm()
    # return render(request, 'index.html', {'title': 'HOME', 'form': form, })

    # from designweb.tests import test_payment
    # transaction_object = {
    #     "amount":
    #         {
    #             "total": "25.55",
    #             "currency": "USD",
    #             "details": {
    #                 "subtotal": "25.00",
    #                 "tax": "0.05",
    #                 "shipping": "0.50"
    #             }
    #         },
    #     "description": "This is the payment transaction description."
    # }
    #
    # card_info = {
    #     "credit_card": {
    #         "type": "visa",
    #         "number": "4032035160291142",  # "4032035160291142",4417119669820331
    #         "expire_month": "03",
    #         "expire_year": "2020",
    #         "cvv2": "874",
    #         "first_name": "Joe",
    #         "last_name": "Shopper",
    #         "billing_address": {
    #             "line1": "52 N Main ST",
    #             "city": "Johnstown",
    #             "state": "OH",
    #             "postal_code": "43210",
    #             "country_code": "US"
    #         }
    #     }
    # }
    # test_payment('credit_card', request.META['HTTP_HOST'], transaction_object, card_info)

    from designweb.utils import get_recommended_products_by_product
    product = get_object_or_404(Product, pk=10)

    print(get_recommended_products_by_product(product))

    return render(request, 'index.html', {'title': 'HOME', })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            user.user_profile = UserProfile.objects.create(user=user)
            user.cart = Cart.objects.create(user=user)
            user.wish_list = WishList.objects.create(user=user)
            # sending_mail_for_new_signup(username)
            login(request, user)
            return render(request, 'home.html', get_display_dict(title='HOME',
                                                                 pass_dict={'welcome': True, 'user_id': user.pk}))
        else:
            pass_dicts = {'form': form, 'error_msg': form.error_messages}
            return render(request, 'signup.html', get_display_dict('SIGNUP', pass_dict=pass_dicts))
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', get_display_dict('SIGNUP', pass_dict={'form': form, }))


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if not user:
            return redirect(reverse('design:home'), get_display_dict(title='Home'))
        elif user.is_authenticated():
            login(request, user)
            return redirect(reverse('design:home'), get_display_dict(title='HOME', pass_dict={'user_id': user.pk, }))
    else:
        return render(request, 'login.html', get_display_dict(title='LOGIN'))


def logout_view(request):
    logout(request)
    return redirect(reverse('design:home'))


# first show up for new register customer
@login_required(login_url='/login/')
@api_view(['GET', 'POST', ])
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user is not None:
            user.user_profile.gender = request.POST['gender']
            user.user_profile.designer_type = request.POST['designer_type']
            user.user_profile.address1 = request.POST['address1']
            user.user_profile.address2 = request.POST['address2']
            user.user_profile.city = request.POST['city']
            user.user_profile.state = request.POST['state']
            user.user_profile.zip = request.POST['zip']
            user.user_profile.save()
            return redirect(reverse('design:home'), get_display_dict('HOME'))

    pass_dicts = {'designer_type': user.user_profile.designer_type,
                  'gender': user.user_profile.gender,
                  'address1': user.user_profile.address1,
                  'address2': user.user_profile.address2,
                  'city': user.user_profile.city,
                  'state': user.user_profile.state,
                  'zip': user.user_profile.zip,
                  'user_id': user.pk, }
    return render(request, 'user_profile.html', get_display_dict('USER PROFILE', pass_dict=pass_dicts))


@ensure_csrf_cookie
def product_view(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    show_create = False
    micro_group = is_user_already_in_group(user, product)
    if micro_group is None:
        show_create = True
    image_dict = get_s3_bucket_image_by_product(product.product_code)
    product_details = product.details
    pass_dicts = {'product': product,
                  'show_create': show_create,
                  'group': micro_group,
                  'is_in_cart': is_product_in_user_cart(user, pk),
                  'product_colors': False,
                  'product_size': False,
                  'product_stock_range': range(1, product.number_in_stock + 1), }
    if product_details.color != '':
        pass_dicts['product_colors'] = product_details.color.split(sep='|')
    if product_details.size != '':
        pass_dicts['product_size'] = product_details.size.split(sep='|')
    if user.is_authenticated():
        pass_dicts['user_id'] = user.pk

    rec_product_dict = get_recommended_products_by_product(product)

    return render(request,
                  'product.html',
                  (get_display_dict('PRODUCT', pass_dict=dict(list(image_dict.items()) + list(pass_dicts.items())))))


"""     --Ajax views--      """


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
def add_cart(request, pk, prod_quantity=1):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    user.cart.products.add(product)
    product_size = request.POST.get('product_size') or ''
    product_color = request.POST.get('product_color') or ''
    if not is_product_in_cart_details(user, product):
        user.cart.cart_details.create(cart=user.cart,
                                      product=product,
                                      number_in_cart=prod_quantity,
                                      color=product_color,
                                      size=product_size)
    else:
        cart_detail = user.cart.cart_details.filter(product=product)[0]
        cart_detail.number_in_cart = prod_quantity
        cart_detail.color = product_color
        cart_detail.size = product_size
        cart_detail.save()
    return Response(data={'Success': 'Success'})


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
def add_wish(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    user.wish_list.products.add(product)
    return Response(data={'Success': 'Success'})


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
def remove_cart(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    user.cart.products.remove(product)
    if is_product_in_cart_details(user, product):
        user.cart.cart_details.filter(product=product).delete()
    return Response(data={'Success': 'Success'})


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
def remove_wish(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    user.wish_list.products.remove(product)
    return Response(data={'Success': 'Success'})


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
@login_required(login_url='/login/')
def update_order_detail(request, pk, num):
    order_detail = get_object_or_404(OrderDetails, pk=pk)
    order_detail.number_items = num
    order_detail.save()
    return Response(data={'Success': 'Success'})


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
@login_required(login_url='/login/')
def update_cart_detail(request, pk, num, order_id=None):
    cart_detail = get_object_or_404(CartDetail, pk=pk)
    cart_detail.number_in_cart = num
    cart_detail.save()
    if order_id:
        order = get_object_or_404(Order, pk=order_id)
        cost_dict = order.get_total_payment()
        cost_dict['Success'] = 'Success'
        return Response(data=cost_dict)
    return Response(data={})


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
def get_cart_drop_down_by_pk(request, pk):
    user = get_object_or_404(User, pk=pk)
    cart = get_object_or_404(Cart, user=user)
    cart_dict = {}
    for detail in cart.cart_details.all():
        product_code = detail.product.product_code
        product_image = get_s3_bucket_main_image_by_product(product_code)
        temp_dict = {
            'product_image': product_image,
            'product_name': detail.product.product_name,
            'product_count': detail.number_in_cart,
        }
        cart_dict[product_code] = temp_dict
    return Response(data=cart_dict)


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
def like_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.number_like += 1
    product.save()
    return Response(data={'Success': 'Success'})


# @ensure_csrf_cookie
# @api_view(['GET', 'POST', ])
# def get_product_review(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     reviews = CustomerReview.objects.filter(product=product)
#     return Response(data={'review_list': reviews})
#     return Response(data={'Success': 'Success'})


def get_product_forum(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product=product)
    return Response(data={'Success': 'Success', 'comments': comments})


@ensure_csrf_cookie
@api_view(['GET', 'POST', ])
def add_product_forum_comment(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    msg = request.POST.get('comment')
    comment = ProductComment.objects.create(product=product, message=msg)
    if user.is_authenticated():
        comment.reviewer_id = user.pk
        comment.reviewer = str.split(user.username, '@')[0]
        comment.save()
    return Response(data={'Success': 'Success'})


# ===============================================
@ensure_csrf_cookie
@login_required(login_url='/login/')
def my_cart(request):
    user = request.user
    if user.is_authenticated():
        products = user.cart.products.all()
        order_dicts = order_view_process(user)
        pass_dicts = {'products': products, 'orders': user.cart.cart_details.all()}
        combine_dicts = dict(list(order_dicts.items()) + list(pass_dicts.items()))
        return render(request, 'mycart.html', get_display_dict('MY CART', pass_dict=combine_dicts))


@ensure_csrf_cookie
@login_required(login_url='/login/')
def my_wish(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user is not None:
        products = user.wish_list.products.all()
        pass_dicts = {'products': products, }
        return render(request, 'mywishlist.html', get_display_dict('MY WISH LIST', pass_dict=pass_dicts))
# ===============================================


def category_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    pass_dicts = {'products': products,
                  'category_id': pk,
                  'category_name': category.category_name,
                  'category_parent': category.parent_category, }
    return render(request, 'category.html', get_display_dict('CATEGORY', pass_dict=pass_dicts))


def micro_group_view(request, product_id, group_id=None):
    product = get_object_or_404(Product, pk=product_id)
    show_join = False
    user = request.user

    if product is None:
        return

    if group_id is None or not isinstance(group_id, int):   # inside call -- create or to product page
        if user.is_authenticated():
            micro_group = is_user_already_in_group(user, product)
            if micro_group is None:
                # create new group for this user
                group_price = product.price * product.group_discount
                micro_group = MicroGroup.objects.create(product=product, owner=user, is_active=True,
                                                        group_price=group_price, group_discount=product.group_discount)
                micro_group.members.add(user)
                # update cache <timestamp_group_cache> & <user_group_cache>
                update_caches_by_new_group(user, micro_group)
            total_members = micro_group.members.count()
            pass_dicts = {'group': micro_group,
                          'product': micro_group.product,
                          'show_join': show_join,
                          'remain_time': micro_group.get_remain_time_by_seconds(),
                          'total_members': total_members, }
            return render(request, 'microgroup.html', get_display_dict('M-GROUP', pass_dict=pass_dicts))
        else:
            return redirect(reverse('design:login'), get_display_dict('LOGIN'))
    else:   # outside call -- group page or to product page
        group = get_object_or_404(MicroGroup, pk=group_id)
        if group is not None:
            total_members = group.members.count()
            if not group.objects.filter(user=user).exists():
                show_join = True
            pass_dicts = {'group': group,
                          'product': group.product[0],
                          'show_join': show_join,
                          'remain_time': group.get_remain_time_by_seconds(),
                          'total_members': total_members, }
            return render(request, 'microgroup.html', get_display_dict('M-GROUP', pass_dict=pass_dicts))
        else:
            return redirect(reverse('design:product-view', kwargs={'pk': product_id}), get_display_dict('PRODUCT'))


@ensure_csrf_cookie
@login_required(login_url='/login/')
def update_order_info(request, pk, order_id):
    shipping_data = {
        'shipping_address1': request.POST.get('shipping_address1'),
        'shipping_address2': request.POST.get('shipping_address2'),
        'shipping_city': request.POST.get('shipping_city'),
        'shipping_state': request.POST.get('shipping_state'),
        'shipping_zip': request.POST.get('shipping_zip'),
        'shipping_phone1': request.POST.get('shipping_phone1'),
        'shipping_phone2': request.POST.get('shipping_phone2'),
        'billing_address1': request.POST.get('billing_address1'),
        'billing_address2': request.POST.get('billing_address2'),
        'billing_city': request.POST.get('billing_city'),
        'billing_state': request.POST.get('billing_state'),
        'billing_zip': request.POST.get('billing_zip'),
        'billing_phone1': request.POST.get('billing_phone1'),
        'billing_phone2': request.POST.get('billing_phone2'),
    }

    msg = update_order_address_info(pk, order_id, shipping_data)
    response_data = {}
    try:
        response_data['result'] = 'writing successful !'
    except:
        response_data['message'] = 'failed processing ...\n' + msg
    return HttpResponse(json.dumps(response_data), content_type='application/json')


# ================ api =======================
class ProductsList(generics.ListAPIView):
    serializer_class = ProductListSerializer
    paginate_by = 15

    def get_queryset(self):
        # products = Product.objects.all()
        products = Product.objects.filter(is_active=True).order_by('-manually_set_prior_level', )
        grid_list = grid_view_shuffle(products)
        return grid_list


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ProductCategory(generics.ListAPIView):
    serializer_class = ProductListSerializer
    # paginate_by_param = 'page_size'
    paginate_by = 15
    # max_paginate_by = 90

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, pk=category_id)
        products = Product.objects.filter(category=category)
        return grid_view_shuffle(products)


class ProductMiddleLevel(generics.ListAPIView):
    serializer_class = ProductListSerializer
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.filter(prior_level=1)


class ProductHighLevel(generics.ListAPIView):
    serializer_class = ProductListSerializer
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.filter(prior_level=0)


class ProductRecList(generics.ListAPIView):
    serializer_class = ProductListSerializer
    paginate_by = 8

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, pk=product_id)
        product_list = get_recommended_products_by_product(product)
        return product_list


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class ProductReviewList(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductReviewSerializer


class CustomerList(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReviewSet(viewsets.ModelViewSet):
    queryset = CustomerReview.objects.all()
    serializer_class = ProductReviewSerializer
    filter_fields = ('product_id', )


class ProductForumList(viewsets.ReadOnlyModelViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductForumListSerializer
    filter_fields = ('product_id', )
    paginate_by = 5


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
# ===============================================


# ==================== payment pages =============
# for paypal redirect usage
def payment_view(request):
    from designweb.payment.payment_utils import payment_execute
    payment_dict = payment_execute(request.GET['paymentId'], request.GET['PayerID'], request.GET['token'])
    print(payment_dict)
    return redirect(reverse('design:payment-success'),
                    get_display_dict(title='Payment Success', pass_dict=payment_dict))


def payment_success(request):
    return render(request, 'payment/payment_success.html', get_display_dict(title='Payment Success'))


def payment_failed(request):
    return render(request, 'payment/payment_fail.html', get_display_dict(title='Payment Failed'))


def checkout(request):
    order_id = int(request.POST['order_id'])
    order = get_object_or_404(Order, pk=order_id)
    if request.method != 'POST' or not order_id:
        return redirect(reverse('design:payment-failed'), get_display_dict(title='Payment Failed'))
    payment_method = request.POST['payment_method']
    direct_credit_dict = {}
    transaction_dict = {
        "amount":
            {
                "total": str(order.subtotal),
                "currency": "USD",
                "details": {
                    "subtotal": str(order.total_amount - order.total_discount),
                    "tax": str(order.total_tax),
                    "shipping": str(order.total_shipping)
                },
            },
        "description": "creating a payment"
    }
    if payment_method == DIRECT_CREDIT:
        direct_credit_dict = {
            "credit_card": {
                "type": "visa",
                "number": str(request.POST['card_num_1']) +             # "4032035160291142"
                str(request.POST['card_num_2']) +
                str(request.POST['card_num_3']) +
                str(request.POST['card_num_4']),
                "expire_month": str(request.POST['cc_exp_mo']),
                "expire_year": str(request.POST['cc_exp_yr']),
                "cvv2": str(request.POST['cvv_number']),
                "first_name": str(request.POST['card_holder']),     # need split later
                "last_name": "Shopper",
                "billing_address": {
                    "line1": order.billing_address1,
                    "city": order.billing_city,
                    "state": order.billing_state,
                    "postal_code": order.billing_zip,
                    "country_code": "US"
                }
            }
        }

    payment_dict = payment_process(payment_method, request.META['HTTP_HOST'], transaction_dict, direct_credit_dict)
    if not payment_dict:
        return redirect(reverse('design:payment-failed'), get_display_dict(title='Payment Failed'))
    redirect_url = payment_dict['redirect_url']
    if redirect_url:    # payment method is paypal
        return HttpResponseRedirect(redirect_url)
    else:
        print(payment_dict)
        return redirect(reverse('design:payment-success'),
                        get_display_dict(title='Payment Success', pass_dict=payment_dict))
# ===============================================


# ============= Static pages ====================
def about_us(request):
    return render(request, 'articles/about.html', get_display_dict(title='ABOUT US'))


def terms_and_conditions(request):
    return render(request, 'articles/terms.html', get_display_dict(title='TERMS AND CONDITIONS'))


def contact_us(request):
    return render(request, 'articles/contact.html', get_display_dict(title='CONTACT US'))

