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
    title = models.CharField(max_length=255, )
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.created_at}"


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


class Ticket(models.Model):
    movie_session = models.OneToOneField(to=MovieSession,
                                         on_delete=models.CASCADE)
    order = models.OneToOneField(to=Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self) -> None:
        cinema_hall = self.movie_session.cinema_hall

        if self.row < 1 or self.row > cinema_hall.rows:
            raise ValidationError(
                f"Row {self.row} is out of range. "
                f"Valid rows are 1 to {cinema_hall.rows}."
            )

        if self.seat < 1 or self.seat > cinema_hall.seats_in_row:
            raise ValidationError(
                f"Seat {self.seat} is out of range."
                f" Valid seats are 1 to {cinema_hall.seats_in_row}."
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

        class Meta:
            constraints = [
                UniqueConstraint(
                    fields=["movie_session", "row", "seat"],
                    name="unique_movie_session"
                )
            ]

    def __str__(self) -> str:
        return f"{self.movie_session} {str(self.row)} {str(self.seat)}"


class User(AbstractUser):
    pass
