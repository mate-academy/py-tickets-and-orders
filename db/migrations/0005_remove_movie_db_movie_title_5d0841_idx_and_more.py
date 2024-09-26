# Generated by Django 4.0.2 on 2023-03-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_ticket_unique_ticket'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='movie',
            name='db_movie_title_5d0841_idx',
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
