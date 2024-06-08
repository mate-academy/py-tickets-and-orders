from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


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
        indexes = [
            models.Index(fields=["title"])
        ]

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


class User(AbstractUser):
    first_name = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    last_name = models.CharField(
        max_length=255, blank=True, null=True, default=""
    )
    email = models.EmailField(null=True, blank=True, default="")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        to=Order,
        related_name="tickets",
        on_delete=models.CASCADE
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None | Exception:
        if not isinstance(self.row, int) or not isinstance(self.seat, int):
            raise ValidationError("type of row or seat must be integer")

        if not (1 <= self.row <= self.movie_session.cinema_hall.rows):
            raise ValidationError(
                {
                    "row": [
                        "row number must be in "
                        "available range: (1, rows): "
                        f"(1, {self.movie_session.cinema_hall.rows})"
                    ]
                }
            )

        if not (
            1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row
        ):
            raise ValidationError(
                {
                    "seat": [
                        "seat number must be in "
                        "available range: (1, seats_in_row): "
                        f"(1, {self.movie_session.cinema_hall.seats_in_row})"
                    ]
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="row-seat-session"
            )
        ]
