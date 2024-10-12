# Generated by Django 5.1.2 on 2024-10-11 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_remove_movie_db_movie_title_5d0841_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(to='db.actor'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='db.genre'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='actor',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(),
        ),
    ]
