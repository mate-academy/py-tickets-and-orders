from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(to="Actor")
    genres = models.ManyToManyField(to="Genre")

    class Meta:
        indexes = [
            models.Index(fields=["title"])
        ]

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="cinema_halls"
    )
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to="User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to="MovieSession",
        on_delete=models.CASCADE,
        related_name="movie_sessions",
    )
    order = models.ForeignKey(
        to="Order", on_delete=models.CASCADE, related_name="orders"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "row",
                    "seat",
                    "movie_session",
                ],
                name="unique_row_seat_session",
            )
        ]

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title} "
                f"{self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: bool = None,
            update_fields: bool = None,
    ) -> Ticket:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def clean(self) -> None:
        cinema_hall = self.movie_session.cinema_hall

        row_criteria = 1 <= self.row <= cinema_hall.rows
        seat_criteria = 1 <= self.seat <= cinema_hall.seats_in_row

        if not row_criteria:
            raise ValidationError(
                {
                    "row": [
                        "row number must be in available range: "
                        "(1, rows): "
                        f"(1, {cinema_hall.rows})"
                    ]
                }
            )

        if not seat_criteria:
            raise ValidationError(
                {
                    "seat": [
                        "seat number must be in available range:"
                        " (1, seats_in_row): "
                        f"(1, {cinema_hall.seats_in_row})"
                    ]
                }
            )


class User(AbstractUser):
    pass
