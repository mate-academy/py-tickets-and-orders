from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

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
        to=CinemaHall,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


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

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket"),
        ]

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie} "
            f"{self.movie_session.show_time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"(row: {self.row}, "
            f"seat: {self.seat})"
        )

    @staticmethod
    def create_error_message(
        field_name: str,
        max_value: int
    ) -> dict[str, list[str]]:
        plural_field_name = {"row": "rows", "seat": "seats_in_row"}

        return {
            field_name: [
                f"{field_name} number must be in available range: "
                f"(1, {plural_field_name.get(field_name)}): (1, {max_value})"
            ]
        }

    def validate(
        self,
        value_name: str,
        current_value: int,
        available_value: int
    ) -> None:
        if not 1 <= current_value <= available_value:
            raise ValidationError(
                self.create_error_message(
                    value_name,
                    available_value,
                )
            )

    def clean(self) -> None:
        cinema_hall = self.movie_session.cinema_hall

        self.validate(
            "seat",
            self.seat,
            cinema_hall.seats_in_row
        )

        self.validate(
            "row",
            self.row,
            cinema_hall.rows
        )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class User(AbstractUser):
    pass
