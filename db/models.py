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
    actors = models.ManyToManyField(to="db.Actor", related_name="movies")
    genres = models.ManyToManyField(to="db.Genre", related_name="movies")

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
        to="db.CinemaHall",
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to="db.Movie",
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to="db.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to="db.MovieSession",
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(to="db.Order", on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"], name="place_check"
            )
        ]

    @staticmethod
    def generate_error_message(field: str, valid_range: int) -> dict:
        range_names = {
            "seat": "seats_in_row",
            "row": "rows"
        }
        range_name = range_names.get(field, "???")

        return {
            field: [
                f"{field} number must be in available range: "
                f"(1, {range_name}): (1, {valid_range})"
            ]
        }

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall

        if self.seat > hall.seats_in_row:
            raise ValidationError(
                self.generate_error_message("seat", hall.seats_in_row)
            )
        elif self.row > hall.rows:
            raise ValidationError(
                self.generate_error_message("row", hall.rows)
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f"{self.movie_session.movie} {self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")
