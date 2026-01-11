import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from typing import Any
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


now = datetime.datetime.now()


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(default=90)
    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField("Actor", blank=True)

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey("MovieSession",
                                      on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_per_session"
            )
        ]

    def clean(self) -> None:
        max_rows = self.movie_session.cinema_hall.rows
        max_seats = self.movie_session.cinema_hall.seats_in_row

        errors = {}

        if not (1 <= self.row <= max_rows):
            errors["row"] = [
                f"row number must be in available range: "
                f"(1, rows): (1, {max_rows})"
            ]
        if not (1 <= self.seat <= max_seats):
            errors["seat"] = [
                f"seat number must be in available range: "
                f"(1, seats_in_row): (1, {max_seats})"
            ]
        if errors:
            raise ValidationError(errors)

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    movie = models.ForeignKey("Movie",
                              on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey("CinemaHall",
                                    on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self) -> str:
        return (f"{self.movie.title} "
                f"in {self.cinema_hall.name} at {self.show_time}")
