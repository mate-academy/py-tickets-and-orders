# Generated by Django 4.0.2 on 2023-10-08 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_alter_user_first_name_alter_user_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
    ]
