# Generated by Django 5.1.4 on 2024-12-11 09:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_clientaddress_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clientaddress',
            unique_together={('address', 'client')},
        ),
    ]