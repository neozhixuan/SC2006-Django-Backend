# Generated by Django 3.2.3 on 2023-11-02 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_delete_choice_delete_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CompanyName', models.CharField(max_length=100)),
                ('ItemName', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='orderdata',
            name='EntryDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Suggestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemName', models.CharField(max_length=64)),
                ('SuggestionList', models.ManyToManyField(related_name='suggested_lists', to='backend.OrderData')),
            ],
        ),
        migrations.CreateModel(
            name='Predictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ConfidenceScore', models.IntegerField()),
                ('PredictedStockLevel', models.ManyToManyField(related_name='predicted_stock_levels', to='backend.OrderData')),
            ],
        ),
        migrations.AddField(
            model_name='orderdata',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='backend.inventory'),
        ),
    ]