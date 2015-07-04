from django.contrib.auth.models import User, Group
from rest_framework import serializers
from designweb.models import Product, Cart, WishList, CustomerReview, ProductComment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='design:product-detail')

    class Meta:
        model = Product
        fields = ('pk', 'url', 'product_name', 'product_code', 'image_root', 'is_active', 'price', 'sales_price', )


class ProductDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('pk', 'product_name', 'product_code', 'price', 'description', 'is_customize', 'shipping_msg',
                  'important_msg', 'image_root', 'is_active', 'average_review_score', 'sales_price', )


class CartSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedIdentityField(view_name='design:product-detail', many=True)

    class Meta:
        model = Cart
        fields = ('user', 'products', )


class WishListSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedIdentityField(view_name='design:product-detail', many=True)

    class Meta:
        model = WishList
        fields = ('user', 'products', )


class ProductReviewSerializer(serializers.HyperlinkedModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.pk')
    customer_id = serializers.ReadOnlyField(source='customer.pk')
    product_name = serializers.ReadOnlyField(source='product.product_name')
    customer_name = serializers.ReadOnlyField(source='customer.username')
    review_message = serializers.ReadOnlyField(source='message')

    class Meta:
        model = CustomerReview
        fields = ('pk', 'product_id', 'customer_id', 'product_name', 'customer_name', 'review_message', )


class ProductForumListSerializer(serializers.HyperlinkedModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.pk')
    product_name = serializers.ReadOnlyField(source='product.product_name')
    comments = serializers.ReadOnlyField(source='message')

    class Meta:
        model = ProductComment
        fields = ('pk', 'product_id', 'product_name', 'reviewer', 'reviewer_id', 'comments', )