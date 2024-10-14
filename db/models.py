from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default="Unknown")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)

    def __str__(self) -> str:
        show_time_str = self.show_time.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.movie.title} {show_time_str}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders"
    )

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        if not 1 <= self.row <= self.movie_session.cinema_hall.rows:
            raise ValidationError(
                {
                    "row": (
                        f"Row number must be in available range: "
                        f"(1, {self.movie_session.cinema_hall.rows})"
                    )
                }
            )
        if not 1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row:
            raise ValidationError(
                {
                    "seat": (
                        f"Seat number must be in available range: "
                        f"(1, {self.movie_session.cinema_hall.seats_in_row})"
                    )
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_for_movie_session"
            )
        ]
