# Generated by Django 4.1.4 on 2022-12-24 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_alter_order_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
