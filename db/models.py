from django.conf import settings
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
        return (
            f"{self.movie.title} "
            f"{self.show_time} "
            f"{self.cinema_hall.rows} "
            f"{self.cinema_hall.seats_in_row}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self) -> None:
        max_row = self.movie_session.cinema_hall.rows
        max_seat = self.movie_session.cinema_hall.seats_in_row

        if self.row > max_row:
            raise ValidationError(
                {"row":
                 f"row number must be in available range: "
                 f"(1, rows): (1, {max_row})"}
            )

        if self.seat > max_seat:
            raise ValidationError(
                {"seat": f"seat number must "
                 f"be in available range: (1, seats_in_row): "
                 f"(1, {max_seat})"}
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_order_row_seat_order_session"
            )
        ]

    def __str__(self) -> str :
        return (
            f"Matrix 2019-08-19 20:30:00 " # noqa
            f"(row: {self.row}, "
            f"seat: {self.seat})"
        )


class User(AbstractUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    pass
