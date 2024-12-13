# Generated by Django 5.1.4 on 2024-12-13 10:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restaurants', '0004_restaurantmodel_delivery_price_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_amount', models.DecimalField(decimal_places=0, max_digits=10)),
                ('delivery_address', models.CharField(max_length=255)),
                ('delivery_time', models.DateTimeField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('CASH', 'CASH'), ('CLICK', 'CLICK'), ('PAYME', 'PAYME')], default='CASH')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('IN_PROGRESS', 'IN_PROGRESS'), ('DELIVERED', 'DELIVERED'), ('CANCELLED', 'CANCELLED')], default='PENDING')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='restaurants.branchmodel')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
