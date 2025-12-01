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
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="orders")


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(to=MovieSession, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="tickets")
    row = models.IntegerField()
    seat = models.IntegerField()


    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "movie_session"], name="unique_row_seat"),
        ]

    def __str__(self) -> str:
        try:
            return f"{self.movie_session.movie.title} {self.movie_session.show_time} (row: {self.row}, seat: {self.seat})"
        except AttributeError:
            return "Invalid ticket"

    def clean(self) -> None:
        seats_in_row = self.movie_session.cinema_hall.seats_in_row
        rows = self.movie_session.cinema_hall.rows
        errors = {}

        if self.seat < 1 or self.seat > self.movie_session.cinema_hall.seats_in_row:
            raise ValidationError({
                "seat": [
                    f"seat number must be in available range: (1, seats_in_row): (1, {self.movie_session.cinema_hall.seats_in_row})"]
            })
        if self.row < 1 or self.row > self.movie_session.cinema_hall.rows:
            raise ValidationError({
                "row": [f"row number must be in available range: (1, rows): (1, {self.movie_session.cinema_hall.rows})"]
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)


class User(AbstractUser):
    pass



