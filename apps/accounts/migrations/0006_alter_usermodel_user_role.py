# Generated by Django 5.1.4 on 2024-12-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_usermodel_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_role',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('OWNER', 'OWNER'), ('MANAGER', 'MANAGER'), ('COURIER', 'COURIER'), ('CLIENT', 'CLIENT')], default='CLIENT', max_length=50),
        ),
    ]
