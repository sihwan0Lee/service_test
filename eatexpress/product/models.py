from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='상품명')
    manufacturer = models.CharField(max_length=20, verbose_name='제조사')
    stock = models.IntegerField(verbose_name='재고수량')
    unit_price = models.IntegerField(verbose_name='단가')
    expiration_date = models.DateTimeField(
        auto_now_add=True, verbose_name='유통기한')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name = '상품'
        verbose_name_plural = '상품'
