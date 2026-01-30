from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("first_name", "last_name")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CinemaHall(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    duration = models.IntegerField()

    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")

    def __str__(self) -> str:
        return self.title


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")
    cinema_hall = models.ForeignKey(
        CinemaHall, on_delete=models.CASCADE, related_name="sessions"
    )

    def __str__(self) -> str:
        show_time = self.show_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.movie.title} {show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("db.User", on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Order: {self.created_at:%Y-%m-%d %H:%M:%S}>"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_place_per_session",
            )
        ]

    def __str__(self) -> str:
        show_time = self.movie_session.show_time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"<Ticket: {self.movie_session.movie.title} {show_time} "
            f"(row: {self.row}, seat: {self.seat})>"
        )

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall

        if self.row < 1 or self.row > hall.rows:
            raise ValidationError(
                {
                    "row": [
                        "row number must be in available range: "
                        f"(1, rows): (1, {hall.rows})"
                    ]
                }
            )

        if self.seat < 1 or self.seat > hall.seats_in_row:
            raise ValidationError(
                {
                    "seat": [
                        "seat number must be in available range: "
                        f"(1, seats_in_row): (1, {hall.seats_in_row})"
                    ]
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
