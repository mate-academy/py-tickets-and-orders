from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["row", "seat", "movie_session"],
                                    name="unique_ticket")
        ]

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title}"
                f" {self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:
        numbers_of_row = self.movie_session.cinema_hall.rows
        if not (0 <= self.row <= numbers_of_row):
            raise ValidationError({
                "row": ["row number must be in available "
                        f"range: (1, rows): "
                        f"(1, {numbers_of_row})"]
            })

        seats_in_row = self.movie_session.cinema_hall.seats_in_row
        if not (0 <= self.seat <= seats_in_row):
            raise ValidationError({
                "seat": ["seat number must be in available "
                         f"range: (1, seats_in_row): "
                         f"(1, {seats_in_row})"]
            })

    def save(
            self,
            force_insert: Optional[bool] = False,
            force_update: Optional[bool] = False,
            using: Optional[str] = None,
            update_fields: Optional[list] = None
    ) -> None:
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)


class User(AbstractUser):
    pass
