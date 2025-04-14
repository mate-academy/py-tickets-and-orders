from datetime import datetime

from django.conf import settings
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
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(
        to=Actor,
        related_name="movies"
    )
    genres = models.ManyToManyField(
        to=Genre,
        related_name="movies"
    )

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
        to=CinemaHall,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return (f"{self.movie.title} "
                f"{datetime.strftime(self.show_time, '%Y-%m-%d %H:%M:%S')}")


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return datetime.strftime(self.created_at, "%Y-%m-%d %H:%M:%S")


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_row_seat"
            )
        ]

    def __repr__(self) -> str:
        return (
            f"{self.movie_session} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def __str__(self) -> str:
        return (
            f"{self.movie_session} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        number_rows = self.movie_session.cinema_hall.rows
        number_seats = self.movie_session.cinema_hall.seats_in_row
        errors = {}

        if self.seat not in range(1, number_seats + 1):
            errors["seat"] = [
                f"seat number must be in available range: "
                f"(1, seats_in_row): "
                f"(1, {number_seats})"
            ]
            raise ValidationError(errors)

        if self.row not in range(1, number_rows + 1):
            errors["row"] = [
                f"row number must be in available range:"
                f" (1, rows): (1, {number_rows})"
            ]
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)
