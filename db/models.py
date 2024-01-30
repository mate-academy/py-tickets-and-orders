from typing import Any

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
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

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

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    movie_session = models.ForeignKey(
        "MovieSession",
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=[
                "row",
                "seat",
                "movie_session"
            ],
                name="Unique seat and row")
        ]

    def clean(self) -> None:
        max_seats = self.movie_session.cinema_hall.seats_in_row
        max_rows = self.movie_session.cinema_hall.rows
        if not (1 <= self.row <= max_rows):
            raise ValidationError({
                "row": [
                    f"row number must be in available range:"
                    f" (1, rows):"
                    f" (1, {max_rows})"]
            })

        if not (1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row):
            raise ValidationError({
                "seat": [
                    f"seat number must be in available range:"
                    f" (1, seats_in_row): (1, {max_seats})"
                ]
            })

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: Any = None,
            update_fields: Any = None
    ) -> None:
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        movie = self.movie_session.__str__()
        return f"{movie} (row: {self.row}, seat: {self.seat})"


class User(AbstractUser):
    pass
