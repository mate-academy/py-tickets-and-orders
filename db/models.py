# db/models.py
from django.db import models
from django.db.models import Index, UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:  # ANN204 fixed
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:  # ANN204 fixed
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    def __str__(self) -> str:  # ANN204 fixed
        return self.title

    class Meta:
        indexes = [Index(fields=["title"])]


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:  # ANN201 fixed
        return self.rows * self.seats_in_row

    def __str__(self) -> str:  # ANN204 fixed
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:  # ANN204 fixed
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:  # ANN204 fixed
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:  # ANN204 fixed
        data = self.movie_session.show_time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"{self.movie_session.movie.title} "
            f"{data}"
            f" (row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:  # ANN201 fixed
        if not (self.row > 0
                and self.row <= self.movie_session.cinema_hall.rows):
            raise ValidationError({
                "row": "row number must be in available range: (1, rows): "
                f"(1, {self.row - 1})"
            })
        if not (self.seat <= self.movie_session.cinema_hall.seats_in_row
                and self.seat > 0):
            raise ValidationError({
                "seat": "seat number must be in available range:"
                        " (1, seats_in_row): "
                f"(1, {self.seat - 1})"
            })

    def save(self, *args, **kwargs) -> None:  # ANN201 fixed
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_row_seat_movie_session"
            )
        ]
