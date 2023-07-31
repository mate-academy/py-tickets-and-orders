from datetime import datetime
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


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
    title: str = models.CharField(max_length=255, db_index=True)
    description: str = models.TextField()
    actors = models.ManyToManyField(to=Actor)
    genres = models.ManyToManyField(to=Genre)

    def __str__(self) -> str:
        return self.title


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
    show_time: datetime = models.DateTimeField()
    cinema_hall: CinemaHall = models.ForeignKey(
        to=CinemaHall,
        on_delete=models.CASCADE
    )
    movie: Movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class Ticket(models.Model):
    movie_session: MovieSession = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row: int = models.IntegerField()
    seat: int = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_active"
            )
        ]

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: Any = None,
            update_fields: Any = None
    ) -> None:
        self.full_clean()
        super(Ticket, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def clean(self) -> None:
        if not (1 <= self.row <= self.movie_session.cinema_hall.rows):
            raise ValidationError({
                "row": f"row number must be in available range: "
                       f"(1, rows): "
                       f"(1, {self.row - 1})"
            })
        if not (1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row):
            raise ValidationError({
                "seat": f"seat number must be in available range: "
                        f"(1, seats_in_row): "
                        f"(1, {self.seat - 1})"
            })

    def __str__(self) -> str:
        title = self.movie_session.movie.title
        time = self.movie_session.show_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{title} {time} (row: {self.row}, seat: {self.seat})"
