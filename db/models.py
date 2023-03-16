from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from settings import AUTH_USER_MODEL


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

    actors = models.ManyToManyField(to=Actor)
    genres = models.ManyToManyField(to=Genre)

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"])
        ]
        default_related_name = "movies"


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
    cinema_hall = models.ForeignKey(to=CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "moviesessions"

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        default_related_name = "orders"

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()

    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_seat_session")
        ]
        default_related_name = "tickets"

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} (row: {self.row},"
            f" seat: {self.seat})"
        )

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall
        if not (1 <= self.seat <= hall.seats_in_row):
            raise ValidationError({
                "seat": f"seat number must be in available range: "
                        f"(1, seats_in_row): "
                        f"(1, {hall.seats_in_row})"
            })

        if not (1 <= self.row <= hall.rows):
            raise ValidationError({
                "row": f"row number must be in available range: (1, rows): "
                       f"(1, {hall.rows})",
            })

    def save(
        self, force_insert: bool = False, force_update: bool = False,
        using: bool = None, update_fields: bool = None
    ) -> "Ticket":

        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)


class User(AbstractUser):
    pass
