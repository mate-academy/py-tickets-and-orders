# db/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint


class User(AbstractUser):
    pass


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self):
        return (f"{self.movie_session.movie.title} "
                f"{self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self):
        cinema_hall = self.movie_session.cinema_hall
        if self.row > cinema_hall.rows or self.row < 1:
            raise ValidationError(
                {
                    "row": [
                        f"row number must be in available range: "
                        f"(1, rows): (1, {cinema_hall.rows})"
                    ]
                }
            )
        if self.seat > cinema_hall.seats_in_row or self.seat < 1:
            raise ValidationError(
                {
                    "seat": [
                        f"seat number must be in available range: "
                        f"(1, seats_in_row): (1, {cinema_hall.seats_in_row})"
                    ]
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_seat_per_session"
            )
        ]
