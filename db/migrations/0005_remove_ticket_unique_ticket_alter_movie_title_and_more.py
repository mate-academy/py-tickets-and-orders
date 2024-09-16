# Generated by Django 4.0.2 on 2023-03-26 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_remove_movie_created_at'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ticket',
            name='unique_ticket',
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='row_seat_movie_session'),
        ),
    ]
