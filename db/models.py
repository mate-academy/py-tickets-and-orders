from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Actor(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name="actors")


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="movies")


class MovieSession(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def capacity(self) -> int:
        return self.rows * self.seats_in_row


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"<Order: {self.created_at}>"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )
    movie_session = models.ForeignKey(
        MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    def clean(self) -> None:
        if not (1 <= self.row <= self.movie_session.rows):
            raise ValidationError(
                f"Row {self.row} is out of range for this session."
            )
        if not (1 <= self.seat <= self.movie_session.seats_in_row):
            raise ValidationError(
                f"Seat {self.seat} is out of range for this session."
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        start = self.movie_session.start_time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"<Ticket: {self.movie_session.movie.title} {start} "
            f"(row: {self.row}, seat: {self.seat})>"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_per_seat",
            )
        ]
