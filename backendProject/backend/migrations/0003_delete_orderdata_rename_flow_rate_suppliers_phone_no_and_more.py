# Generated by Django 4.2.7 on 2023-11-13 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_suppliers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderData',
        ),
        migrations.RenameField(
            model_name='suppliers',
            old_name='flow_rate',
            new_name='phone_no',
        ),
        migrations.RemoveField(
            model_name='predictions',
            name='items_data',
        ),
        migrations.AddField(
            model_name='predictions',
            name='item_name',
            field=models.CharField(default='default_value', max_length=100),
        ),
        migrations.AddField(
            model_name='predictions',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='suppliers',
            name='item_sold',
            field=models.CharField(default='default_value', max_length=100),
        ),
    ]