# Generated by Django 5.1.4 on 2024-12-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0007_remove_restaurantmodel_delivery_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantmodel',
            name='service_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
