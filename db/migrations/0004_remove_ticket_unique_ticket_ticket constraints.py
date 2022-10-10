# Generated by Django 4.0.2 on 2022-06-23 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_ticket_unique'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ticket',
            name='unique',
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat', 'movie_session'), name='ticket constraints'),
        ),
    ]
