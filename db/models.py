from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import PROTECT, CASCADE, UniqueConstraint

import settings


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


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Order: {self.created_at}>"


class Ticket(models.Model):
    movie_session = models.ForeignKey(to=MovieSession, on_delete=CASCADE)
    order = models.ForeignKey(to=Order, on_delete=CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (f"<Ticket: {self.movie_session.movie.title}"
                f" {self.order.created_at} (row: {self.row},"
                f" seat: {self.seat})>")

    def clean(self) -> None:
        if ((self.row <= self.movie_session.cinema_hall.rows)
                and (self.seat <= self.movie_session.cinema_hall.seats_in_row)):
            raise ValidationError({
                "row": [f"row number must be in available range: "
                        f"(1, rows): (1, {self.movie_session.cinema_hall.rows})"],
                "seat": [f"row number must be in available range: "
                         f"(1, seat_in_row): (1, {self.movie_session.cinema_hall.seats_in_row})"]
            })

    def save(
        self, force_insert=False, force_update=False, using=None, update_field=False
    ):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_field)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "movie_session"], name="unique_ticket")
        ]


class User(AbstractUser):
    pass




