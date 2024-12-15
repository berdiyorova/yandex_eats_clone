# Generated by Django 5.1.4 on 2024-12-15 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_ordermodel_courier'),
        ('restaurants', '0008_alter_restaurantmodel_service_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch', to='restaurants.branchmodel'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('ACCEPTED', 'ACCEPTED'), ('IN_TRANSIT', 'IN_TRANSIT'), ('DELIVERED', 'DELIVERED'), ('CANCELLED', 'CANCELLED')], default='PENDING'),
        ),
    ]