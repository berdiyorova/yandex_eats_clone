# Generated by Django 5.1.4 on 2024-12-14 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_rename_employee_branchmodel_manager_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchmodel',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
