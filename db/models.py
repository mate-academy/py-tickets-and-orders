from __future__ import annotations

from typing import Optional
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint
from django.db import models

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
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)

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
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        self.created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class User(AbstractUser):
    pass


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title}"
                f" {self.movie_session.show_time}"
                f" (row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:
        if not self.row <= self.movie_session.cinema_hall.rows:
            raise ValidationError(
                {
                    "row": f"row number must be in available range: "
                           f"(1, rows): (1, "
                           f"{self.movie_session.cinema_hall.rows})"
                }
            )
        if not self.seat <= self.movie_session.cinema_hall.seats_in_row:
            raise ValidationError(
                {
                    "seat": f"seat number must be in available range:"
                            f" (1, seats_in_row): (1, "
                            f"{self.movie_session.cinema_hall.seats_in_row})"
                }
            )

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: Optional = None,
            update_fields: Optional = None
    ) -> Ticket:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
        )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_row_seat_and_movie_session"
            )
        ]
