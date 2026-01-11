from django.utils import timezone

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
    class Meta:
        indexes = [
            models.Index(fields=["title"])
        ]

    title = models.CharField(max_length=255)
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
    class Meta:
        ordering = ["-created_at"]
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "movie_session"],
                             name="unique_row_seat_movie_session")
        ]

    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self) -> None:
        errors = {}

        if not (0 < self.row <= self.movie_session.cinema_hall.rows):
            errors["row"] = [
                f"row number must be in available range: "
                f"(1, rows): (1, {self.movie_session.cinema_hall.rows})"
            ]

        if not (0 < self.seat <= self.movie_session.cinema_hall.seats_in_row):
            errors["seat"] = [
                f"seat number must be in available range: "
                f"(1, seats_in_row): "
                f"(1, {self.movie_session.cinema_hall.seats_in_row})"
            ]

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.movie_session} (row: {self.row}, seat: {self.seat})"


class User(AbstractUser):
    pass
