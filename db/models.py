from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

import settings


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

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"])
        ]


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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.movie_session} (row: {self.row}, seat: {self.seat})"

    def clean(self) -> None:
        if not (1 <= self.row <= self.movie_session.cinema_hall.rows):
            raise ValidationError({"row": [
                "row number must be in available range: (1, rows): "
                f"(1, {self.movie_session.cinema_hall.rows})"
            ]})
        if not (1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row):
            raise ValidationError({"seat": [
                "seat number must be in available range: (1, seats_in_row): "
                f"(1, {self.movie_session.cinema_hall.seats_in_row})"
            ]})

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: Any = None,
            update_fields: Any = None
    ) -> super:
        self.full_clean()
        return super(Ticket, self).save(force_insert,
                                        force_update,
                                        using,
                                        update_fields)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_row_seat"
            )
        ]


class User(AbstractUser):
    pass
