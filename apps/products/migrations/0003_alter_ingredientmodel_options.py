# Generated by Django 5.1.4 on 2024-12-15 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_rename_mass_productmodel_measure_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientmodel',
            options={'verbose_name': 'Ingredient', 'verbose_name_plural': 'Ingredients'},
        ),
    ]