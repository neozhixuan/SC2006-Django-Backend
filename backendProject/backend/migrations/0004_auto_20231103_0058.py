# Generated by Django 3.2.3 on 2023-11-02 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20231103_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdata',
            name='FoodCategory',
        ),
        migrations.RemoveField(
            model_name='orderdata',
            name='inventory',
        ),
    ]
