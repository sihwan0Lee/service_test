from django.contrib import admin
from .models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'stock',
                    'unit_price', 'expiration_date',)


admin.site.register(Product, ProductAdmin)
