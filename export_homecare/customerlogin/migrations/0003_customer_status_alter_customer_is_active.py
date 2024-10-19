# Generated by Django 4.2.1 on 2024-07-07 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerlogin', '0002_alter_customer_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]