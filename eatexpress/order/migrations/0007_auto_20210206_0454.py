# Generated by Django 3.1.6 on 2021-02-06 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210206_0445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderproduct',
            options={'verbose_name': '주문 상품', 'verbose_name_plural': '주문 상품'},
        ),
    ]
