# Generated by Django 5.1.4 on 2024-12-15 03:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_ordermodel_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='delivery_address',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='delivery_time',
        ),
        migrations.CreateModel(
            name='OrderItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(max_length=100)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='orders/')),
                ('product_measure', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('measure_unit', models.CharField(max_length=10)),
                ('product_price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.ordermodel')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
            },
        ),
    ]
