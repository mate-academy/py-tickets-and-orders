# Generated by Django 4.1.4 on 2022-12-29 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_alter_ticket_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-movie_session']},
        ),
    ]
