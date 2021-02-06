from django.db import models
from user.models import User
from product.models import Product


class Order(models.Model):
    username = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, verbose_name='회원')
    products = models.ManyToManyField(
        'product.Product', through='OrderProduct', verbose_name='상품명')
    total_price = models.IntegerField(verbose_name='총 가격', default="0")
    ordered_date = models.DateTimeField(
        auto_now_add=True, verbose_name='주문 날짜')
    status = models.CharField(max_length=8, verbose_name='주문상태', choices=(
        ('yes', 'yes'), ('no', 'no')), default='no')

    def __str__(self):
        return str(self.username.email) + '/' + str(self.ordered_date) + '/' + str(self.status)

    class Meta:
        db_table = 'orders'
        verbose_name = '주문 장바구니'
        verbose_name_plural = '주문 장바구니'


class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='주문갯수')

    class Meta:
        db_table = 'order_products'
        verbose_name = "주문 상품"
        verbose_name_plural = "주문 상품"
