# Generated by Django 5.1.4 on 2024-12-15 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_ordermodel_branch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitemmodel',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]