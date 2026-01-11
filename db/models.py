from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


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
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(
        to="Actor",
        related_name="movies"
    )
    genres = models.ManyToManyField(
        to="Genre",
        related_name="movies"
    )

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to="CinemaHall",
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to="Movie",
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    def __str__(self) -> str:
        movie_title = self.movie_session.movie.title
        show_time = self.movie_session.show_time
        row = self.row
        seat = self.seat
        return (
            f"{movie_title} "
            f"{show_time} "
            f"(row: {row}, seat: {seat})"
        )

    def clean(self) -> None:
        max_row = self.movie_session.cinema_hall.rows
        max_seat = self.movie_session.cinema_hall.seats_in_row

        if self.row < 1 or self.row > max_row:
            raise ValidationError({
                "row": [
                    (
                        "row number must be in available range: (1, rows): "
                        f"(1, {max_row})"
                    )
                ]
            })
        if self.seat < 1 or self.seat > max_seat:
            raise ValidationError({
                "seat": [
                    (
                        "seat number must be in available range: "
                        "(1, seats_in_row): "
                        f"(1, {max_seat})"
                    )
                ]
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_seat_per_movie_session"
            )
        ]
