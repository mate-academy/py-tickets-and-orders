from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model replacing Django's default user."""
    pass


class Genre(models.Model):
    name = models.CharField(max_length=255)

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
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name} ({self.rows}x{self.seats_in_row})"


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="sessions")
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    def __str__(self) -> str:
        return (
            f"{self.movie.title} at "
            f"{self.show_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Order: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}>"


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_per_session",
            )
        ]

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall

        if not (1 <= self.row <= hall.rows):
            raise ValidationError({
                "row": [
                    (
                        "row number must be in available range: "
                        f"(1, rows): (1, {hall.rows})"
                    )
                ]
            })

        if not (1 <= self.seat <= hall.seats_in_row):
            raise ValidationError({
                "seat": [
                    (
                        "seat number must be in available range: "
                        f"(1, seats_in_row): (1, {hall.seats_in_row})"
                    )
                ]
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        show_time = self.movie_session.show_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        title = self.movie_session.movie.title
        return (
            f"<Ticket: {title} {show_time} "
            f"(row: {self.row}, seat: {self.seat})>"
        )
