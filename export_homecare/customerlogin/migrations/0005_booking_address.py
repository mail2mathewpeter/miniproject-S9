# Generated by Django 4.2.1 on 2024-08-03 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerlogin', '0004_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='address',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
