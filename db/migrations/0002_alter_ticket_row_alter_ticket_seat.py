# Generated by Django 4.0.2 on 2023-09-16 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='row',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat',
            field=models.PositiveIntegerField(),
        ),
    ]
