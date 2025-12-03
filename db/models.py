from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies")
    genres = models.ManyToManyField(Genre, related_name="movies")


class CinemaHall(models.Model):
    name = models.CharField(max_length=50)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="sessions")


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at.strftime("%Y-%m-%d %H:%M:%S"))


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets")
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets")
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_per_seat")
        ]

    def clean(self) -> None:
        if self.movie_session:
            hall = self.movie_session.cinema_hall
            if self.row < 1 or self.row > hall.rows:
                raise ValidationError({
                    "row": [
                        f"row number must be in available range:"
                        f" (1, rows): (1, {hall.rows})"
                    ]
                })
            if self.seat < 1 or self.seat > hall.seats_in_row:
                raise ValidationError({
                    "seat": [
                        f"seat number must be in available range: "
                        f"(1, seats_in_row): (1, {hall.seats_in_row})"
                    ]
                })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"(row: {self.row}, seat: {self.seat})"
        )
