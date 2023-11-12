# Generated by Django 4.2.7 on 2023-11-12 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default='default_value', max_length=100)),
                ('flow_rate', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]