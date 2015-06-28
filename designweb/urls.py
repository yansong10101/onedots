__author__ = 'zys'
from django.conf.urls import url, patterns, include
from designweb import views
from rest_framework import routers

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^user-profile/(?P<pk>[0-9]+)/$', views.user_profile, name='user-profile'),
    url(r'^product/(?P<pk>[0-9]+)/$', views.product_view, name='product-view'),
    # url(r'^cart/', views.my_cart, name='my-cart'),
    url(r'^cart-and-purchase/', views.my_cart, name='cart-and-purchase'),
    url(r'^wish/(?P<pk>[0-9]+)/', views.my_wish, name='my-wish'),
    # url(r'^order/(?P<pk>[0-9]+)/', views.my_order, name='my-order'),
    url(r'^category/(?P<pk>[0-9]+)/', views.category_view, name='category-view'),
    # url(r'^microgroup/(?P<pk>[0-9]+)/(?P<product_id>[0-9]+)/$', views.micro_group_view, name='micro-group'),
    url(r'^microgroup/(?P<product_id>[0-9]+)/(?P<group_id>[0-9]+)/$', views.micro_group_view, name='micro-group-id'),
    url(r'^microgroup/(?P<product_id>[0-9]+)//$', views.micro_group_view, name='micro-group'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^direct-checkout/$', views.checkout_stripe, name='direct-checkout'),

    # api for ajax add and delete
    url(r'^api/cart/(?P<pk>[0-9]+)/add/(?P<prod_quantity>[0-9]+)/$', views.add_cart, name='add-to-cart'),
    url(r'^api/wish/(?P<pk>[0-9]+)/add/$', views.add_wish, name='add-to-wish'),
    url(r'^api/cart/(?P<pk>[0-9]+)/remove/$', views.remove_cart, name='remove-from-cart'),
    url(r'^api/wish/(?P<pk>[0-9]+)/remove/$', views.remove_wish, name='remove-from-wish'),
    url(r'^api/order-detail/(?P<pk>[0-9]+)/(?P<num>[0-9]+)/update/$', views.update_order_detail, name='update-order'),
    url(r'^api/cart-detail/(?P<pk>[0-9]+)/(?P<num>[0-9]+)/update/(?P<order_id>[0-9]+)/$', views.update_cart_detail,
        name='update-cart'),
    url(r'^api/cart-detail/(?P<pk>[0-9]+)/(?P<num>[0-9]+)/update//$', views.update_cart_detail, name='update-cart'),
    url(r'^api/like/(?P<pk>[0-9]+)/$', views.like_product, name='like-product'),
    url(r'^api/address/(?P<pk>[0-9]+)/(?P<order_id>[0-9]+)/$', views.update_order_info, name='shipping-address'),
    # url(r'^api/products-review/(?P<pk>[0-9]+)/$', views.get_product_review, name='product-review'),
    url(r'^api/cart-drop-down/(?P<pk>[0-9]+)/$', views.get_cart_drop_down_by_pk, name='cart-drop-down-list'),
    url(r'^api/forum/add-comment/(?P<product_id>[0-9]+)/$', views.add_product_forum_comment, name='add-comment-to-forum'),

    # api using rest-framework
    url(r'^api/products/$', views.ProductsList.as_view(), name='product-list'),
    url(r'^api/products/(?P<pk>[0-9]+)/$', views.ProductDetail.as_view(), name='product-detail'),
    url(r'^api/auth/user/(?P<pk>[0-9]+)/$', views.CustomerList.as_view(), name='auth-user'),
    url(r'^api/products/filter/(?P<category_id>[0-9]+)/$', views.ProductCategory.as_view(), name='product-category'),
    url(r'^api/products/recommendations/middle-level/$', views.ProductMiddleLevel.as_view(), name='middle-level'),
    url(r'^api/products/recommendations/high-level/$', views.ProductHighLevel.as_view(), name='high-level'),
    url(r'^api/product-page/recommendations/(?P<product_id>[0-9]+)/$', views.ProductRecList.as_view(),
        name='product-page-rec'),

    # payment redirect view
    url(r'^payment/approval/', views.payment_view, name='payment-approval'),
    url(r'^payment/success/', views.payment_success, name='payment-success'),
    url(r'^payment/failed/', views.payment_failed, name='payment-failed'),

    # static pages
    url(r'^article/about-us/', views.about_us, name='about-us'),
    url(r'^article/terms-and-conditions/', views.terms_and_conditions, name='terms-and-conditions'),
    url(r'^article/contact-us/', views.contact_us, name='contact-us'),
)


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'wishlists', views.WishListViewSet)
router.register(r'reviews', views.ReviewSet)
router.register(r'comments', views.ProductForumList)

urlpatterns += patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)