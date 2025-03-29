from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

import settings


class User(AbstractUser):
    pass


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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_seat_row_movie_session",
            )
        ]

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        correct_rows = (
            True if 1 <= self.row <= self.movie_session.cinema_hall.rows
            else False
        )
        correct_seats = (
            True
            if 1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row
            else False
        )

        errors = {}

        if not correct_seats:
            errors["seat"] = (
                f"seat number must be in available range: "
                f"(1, seats_in_row): "
                f"(1, {self.movie_session.cinema_hall.seats_in_row})"
            )
        if not correct_rows:
            errors["row"] = (
                f"row number must be in available range: "
                f"(1, rows): "
                f"(1, {self.movie_session.cinema_hall.rows})"
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{str(self.movie_session.show_time)} "
            f"(row: {self.row}, seat: {self.seat})"
        )
