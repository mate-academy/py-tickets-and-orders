from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


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

    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall,
        related_name="sessions",
        on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        to=Movie,
        related_name="sessions",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=User,
        related_name="orders",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        to=Order,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(name="ticket_constraints",
                                    fields=["row", "seat", "movie_session"]
                                    )
        ]

    def __str__(self) -> str:
        return f"{self.movie_session.movie} {self.movie_session.show_time} " \
               f"(row: {self.row}, seat: {self.seat})"

    def clean(self) -> None:
        rows_in_cinema = self.movie_session.cinema_hall.rows
        seats_in_cinema = self.movie_session.cinema_hall.seats_in_row
        if not (1 <= self.row <= rows_in_cinema):
            raise ValidationError({
                "row": f"row number must be in available range: "
                       f"(1, rows): (1, {rows_in_cinema})"
            })
        if not (1 <= self.seat <= seats_in_cinema):
            raise ValidationError({
                "seat": f"seat number must be in available range: "
                        f"(1, seats_in_row): (1, {seats_in_cinema})"
            })

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: Any = None,
            update_fields: Any = None
    ) -> None:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )
