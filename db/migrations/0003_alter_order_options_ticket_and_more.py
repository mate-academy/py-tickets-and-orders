# Generated by Django 4.0.2 on 2023-07-21 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("db", "0002_order_movie_db_movie_title_5d0841_idx"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("row", models.IntegerField()),
                ("seat", models.IntegerField()),
                (
                    "movie_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="db.moviesession",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="db.order"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("movie_session", "row", "seat"),
                name="unique_ticket_seat_row_movie_session",
            ),
        ),
    ]
