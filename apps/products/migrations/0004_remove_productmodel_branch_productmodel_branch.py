# Generated by Django 5.1.4 on 2024-12-15 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_ingredientmodel_options'),
        ('restaurants', '0008_alter_restaurantmodel_service_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='branch',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='restaurants.branchmodel'),
            preserve_default=False,
        ),
    ]
