# Generated by Django 3.1.3 on 2020-11-29 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productsapp', '0002_auto_20201129_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_products',
        ),
        migrations.AddField(
            model_name='order',
            name='order_products',
            field=models.ManyToManyField(to='Productsapp.OrderProduct'),
        ),
    ]
