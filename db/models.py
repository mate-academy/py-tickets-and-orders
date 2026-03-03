from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name: str = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name: str = models.CharField(max_length=255)
    last_name: str = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title: str = models.CharField(max_length=255)
    description: str = models.TextField()
    actors: models.Manager = models.ManyToManyField(
        to=Actor, related_name="movies")
    genres: models.Manager = models.ManyToManyField(
        to=Genre, related_name="movies")

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"], name="customer_title_idx"),
        ]


class CinemaHall(models.Model):
    name: str = models.CharField(max_length=255)
    rows: int = models.IntegerField()
    seats_in_row: int = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time: models.DateTimeField = models.DateTimeField()
    cinema_hall: models.ForeignKey = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie: models.ForeignKey = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session: models.ForeignKey = models.ForeignKey(
        MovieSession, related_name="tickets", on_delete=models.CASCADE
    )
    order: models.ForeignKey = models.ForeignKey(
        Order, related_name="tickets", on_delete=models.CASCADE
    )
    row: int = models.IntegerField()
    seat: int = models.IntegerField()

    def __str__(self) -> str:
        new_str = (
            f"{self.movie_session.movie.title} {self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )
        return new_str

    def clean(self) -> None:
        cinema_hall = self.movie_session.cinema_hall
        if not (1 <= self.row <= cinema_hall.rows):
            raise ValidationError(
                {
                    "row": [
                        f"row number must be in available range: (1, rows): "
                        f"(1, {cinema_hall.rows})"
                    ]
                }
            )
        if not (1 <= self.seat <= cinema_hall.seats_in_row):
            raise ValidationError(
                {
                    "seat": [
                        f"seat number must be in available range: "
                        f"(1, seats_in_row): (1, {cinema_hall.seats_in_row})"
                    ]
                }
            )

    def save(self, **kwargs: Any) -> None:
        self.full_clean()
        super().save(**kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"], name="unique_fields"
            )
        ]
