from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from typing import Optional
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
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

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
        related_name="movie_sessions",
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title}"
            f" {self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        if not 1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row:
            raise ValidationError(
                {
                    "seat": [
                        f"seat number must be in available range: "
                        f"(1, seats_in_row): "
                        f"(1, {self.seat - 1})"
                    ]
                }
            )

        if not 1 <= self.row <= self.movie_session.cinema_hall.rows:
            raise ValidationError(
                {
                    "row": [
                        f"row number must be in available range: "
                        f"(1, rows): (1, {self.row - 1})"
                    ]
                }
            )

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[list] = None,
    ) -> None:
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        unique_together = ["row", "seat", "movie_session"]


class User(AbstractUser):
    pass
