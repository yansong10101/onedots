from django.contrib import admin
from designweb.models import UserProfile, Product, ProductExtension, Category, Order, OrderDetails, WishList, Cart, \
    CustomerReview, ProductComment
from django.utils.translation import ugettext_lazy

admin.site.site_header = ugettext_lazy('1 dots admin')
admin.site.site_title = ugettext_lazy('One Dots')


class ExtensionProductInline(admin.StackedInline):
    model = ProductExtension


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_code', 'create_date', 'modified_date', 'price', 'is_active',
                    'manually_set_prior_level', )
    list_filter = ('create_date', 'is_active', 'prior_level', )
    filter_horizontal = ('category', )
    ordering = ('-create_date', )

    inlines = [ExtensionProductInline, ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_date', 'modified_date', )
    list_filter = ('created_date', )
    ordering = ('category_name', )


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', )
    filter_horizontal = ('products', )


class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', )
    filter_horizontal = ('products', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )


class ProductForumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'create_date', 'message', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'created_date', 'modified_date', 'total_items', 'is_paid', 'payment_resource', )
    list_filter = ('is_paid', )


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('get_order_id', 'order', 'number_items', 'product', 'shipping_status', 'tracking_code', 'shipping_date',
                    'is_order_paid', 'is_tracking_code_filled', )
    list_select_related = ('is_paid', )


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails, OrderDetailAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Cart, CartAdmin)

admin.site.register(CustomerReview)
admin.site.register(ProductComment, ProductForumAdmin)
