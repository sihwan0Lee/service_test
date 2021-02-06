from django.contrib import admin
from .models import Order, OrderProduct
from user.models import User
from product.models import Product
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'total_price', 'ordered_date',)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
