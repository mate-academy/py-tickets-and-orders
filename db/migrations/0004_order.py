# Generated by Django 4.0.2 on 2023-03-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
