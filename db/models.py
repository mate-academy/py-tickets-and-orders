from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


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
        indexes = [models.Index(fields=["title"], name="title_index")]

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
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE,
        related_name="ticket_sessions"
    )
    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              related_name="ticket_orders")
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_tickets_value"
            )
        ]

    def __str__(self) -> str:
        movie = self.movie_session.movie.title
        session_time = self.movie_session.show_time
        return (f"{movie} {session_time} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:
        super().clean()
        cinema_hall = self.movie_session.cinema_hall
        if cinema_hall.rows < self.row:
            raise ValidationError(
                {
                    "row": [
                        "row number must be in available range: "
                        "(1, rows): "
                        f"(1, {cinema_hall.rows})"
                    ]
                }
            )

        if cinema_hall.seats_in_row < self.seat:
            raise ValidationError(
                {
                    "seat":
                        [
                            "seat number must be in available range: "
                            "(1, seats_in_row): "
                            f"(1, {cinema_hall.seats_in_row})"
                        ]
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
