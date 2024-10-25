# Generated by Django 4.2.1 on 2024-07-08 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('Gender', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='images/')),
            ],
        ),
    ]