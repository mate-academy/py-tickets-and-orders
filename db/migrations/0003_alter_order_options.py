# Generated by Django 4.0.2 on 2023-03-14 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_user_order_ticket_movie_db_movie_title_5d0841_idx_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
    ]
