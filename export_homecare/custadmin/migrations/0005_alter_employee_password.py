# Generated by Django 4.2.1 on 2024-07-09 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custadmin', '0004_employee_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]