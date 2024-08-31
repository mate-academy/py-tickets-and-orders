import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


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
    cinema_hall = models.ForeignKey(
        to=CinemaHall,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ("-created_at",)

    def save(self, **kwargs) -> None:
        if not self.created_at:
            self.created_at = datetime.datetime.now()

        super(Order, self).save(**kwargs)

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class User(AbstractUser):
    pass


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
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["movie_session", "row", "seat"],
                             name="unique_movie_session_row_and_seat"),
        ]

    def clean(self) -> None:
        cinema_hall = self.movie_session.cinema_hall
        errors_dict = {}
        if self.row > cinema_hall.rows:
            errors_dict["row"] = [f"row number must be in available"
                                  f" range: (1, rows): "
                                  f"(1, {cinema_hall.rows})"]
            raise ValidationError(errors_dict)

        if self.seat > cinema_hall.seats_in_row:
            errors_dict["seat"] = [f"seat number must be in available"
                                   f" range: (1, seats_in_row): "
                                   f"(1, {cinema_hall.seats_in_row})"]
            raise ValidationError(errors_dict)

    def save(self, **kwargs) -> None:
        self.full_clean()
        super().save(**kwargs)

    def __str__(self) -> str:
        movie_session = self.movie_session
        return (f"{movie_session.movie.title} {movie_session.show_time}"
                f" (row: {self.row}, seat: {self.seat})")
