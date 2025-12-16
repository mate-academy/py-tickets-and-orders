from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import exceptions

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
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


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
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="row_seat_movie_session_constraint"
            )
        ]

    def clean(self) -> None:
        rows = self.movie_session.cinema_hall.rows
        seats_in_row = self.movie_session.cinema_hall.seats_in_row

        if self.row not in range(1, rows + 1):
            raise exceptions.ValidationError(
                {
                    "row": [
                        "row number must be in available"
                        " range: (1, rows): (1, {})".format(
                            self.movie_session.cinema_hall.rows
                        )
                    ]
                }
            )

        elif self.seat not in range(1, seats_in_row + 1):
            raise exceptions.ValidationError(
                {
                    "seat": [
                        "seat number must be in available"
                        " range: (1, seats_in_row): (1, {})".format(
                            self.movie_session.cinema_hall.seats_in_row
                        )
                    ]
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return "{} {} (row: {}, seat: {})".format(
            self.movie_session.movie.title,
            self.movie_session.show_time,
            self.row,
            self.seat
        )


class User(AbstractUser):
    pass
