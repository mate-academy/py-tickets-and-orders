from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey
from django.db.models.constraints import UniqueConstraint
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
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        ordering = ["-created_at"]  # новіші перші

    def __str__(self) -> str:
        return str(self.created_at)


class User(AbstractUser):
    pass


class Ticket(models.Model):
    movie_session = ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_seat_per_session"
            )
        ]

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall
        if self.row < 1 or self.row > hall.rows:
            raise ValidationError(
                {"row": [f"row number must be in available range: "
                         f"(1, rows): (1, {hall.rows})"]}
            )
        if self.seat < 1 or self.seat > hall.seats_in_row:
            raise ValidationError(
                {"seat": [f"seat number must be in available range: "
                          f"(1, seats_in_row): (1, {hall.seats_in_row})"]}
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title} "
                f"{self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")
