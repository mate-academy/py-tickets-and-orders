from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

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
    actors = models.ManyToManyField(to=Actor)
    genres = models.ManyToManyField(to=Genre)

    class Meta:
        indexes = [models.Index(fields=["title"])]

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
    cinema_hall = models.ForeignKey(to=CinemaHall,
                                    on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "movie_session"],
                             name="unique_ticket")
        ]

    def __str__(self) -> str:
        title = self.movie_session.movie.title
        time = self.movie_session.show_time
        row = self.row
        seat = self.seat
        return f"{title} {time} (row: {row}, seat: {seat})"

    def clean(self) -> Any:
        row_hall = self.movie_session.cinema_hall.rows
        seat_hall = self.movie_session.cinema_hall.seats_in_row
        if not (0 < self.seat <= seat_hall):
            raise ValidationError({
                "seat": ["seat number must be in available "
                         f"range: (1, seats_in_row): (1, {seat_hall})"]
            })
        if not (0 < self.row <= row_hall):
            raise ValidationError({
                "row": ["row number must be in available "
                        f"range: (1, rows): (1, {row_hall})"]
            })

    def save(self,
             force_insert: bool = False,
             force_update: bool = False,
             using: str = None,
             update_fields: list[str] = None) -> Any:
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update,
                                        using, update_fields)


class User(AbstractUser):
    pass
