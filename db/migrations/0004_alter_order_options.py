# Generated by Django 4.0.2 on 2022-10-20 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_alter_order_options_ticket_ticket_unique_ticket'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['created_at']},
        ),
    ]
