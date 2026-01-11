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
        indexes = (models.Index(fields=["title"]),)

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
        to="User", on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return f"{self.created_at}"

    class Meta:
        ordering = ("-created_at",)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("row", "seat", "movie_session"),
                name="unique_ticket",
            ),
        )

    def __str__(self) -> str:
        name = self.movie_session.movie.title
        time = self.movie_session.show_time
        return f"{name} {time} (row: {self.row}, seat: {self.seat})"

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall
        errors = {}
        if self.row > hall.rows:
            errors["row"] = (f"row number must be in available range: "
                             f"(1, rows): (1, {hall.rows})")
        if self.seat > hall.seats_in_row:
            errors["seat"] = (f"seat number must be in available range: "
                              f"(1, seats_in_row): (1, {hall.seats_in_row})")
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class User(AbstractUser):
    pass
