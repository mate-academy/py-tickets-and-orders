from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from django.conf import settings


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
    actors = models.ManyToManyField(to=Actor, related_name="movies_by_actor")
    genres = models.ManyToManyField(to=Genre, related_name="movies_by_genre")

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
        related_name="sessions_by_cinema"
    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        related_name="sessions_by_movie"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders_by_user"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        date_str = self.created_at.strftime("%Y-%m-%d")
        time_str = self.created_at.strftime("%H:%M:%S")
        return f"{date_str} {time_str}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE,
        related_name="session_tickets"
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="tickets_in_order"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self) -> None:
        rows = self.movie_session.cinema_hall.rows
        seats_in_row = self.movie_session.cinema_hall.seats_in_row

        if not (1 <= self.row <= rows):
            raise ValidationError(
                {
                    "row": [
                        f"row number must be in available range: "
                        f"(1, rows): (1, {rows})"
                    ]
                }
            )

        if not (1 <= self.seat <= seats_in_row):
            raise ValidationError(
                {
                    "seat": [
                        f"seat number must be in available range: "
                        f"(1, seats_in_row): (1, {seats_in_row})"
                    ]
                }
            )

    def save(self, *args, **kwargs) -> Optional[None]:
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_row_seat_movie_session"
            )
        ]

    def __str__(self) -> str:
        date_str = self.movie_session.show_time.strftime("%Y-%m-%d")
        time_str = self.movie_session.show_time.strftime("%H:%M:%S")
        return (
            f"{self.movie_session.movie.title} {date_str} {time_str} "
            f"(row: {self.row}, seat: {self.seat})"
        )


class User(AbstractUser):
    pass
