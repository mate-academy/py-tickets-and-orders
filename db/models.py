from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Index


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

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
        indexes = [Index(fields=["title"])]

    def __str__(self) -> str:
        return self.title


class User(AbstractUser):
    pass


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
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
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

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall

        if not (1 <= self.row <= hall.rows):
            raise ValidationError({
                "row": (
                    "row number must be in available range: "
                    f"(1, rows): (1, {hall.rows})"
                )
            })

        if not (1 <= self.seat <= hall.seats_in_row):
            raise ValidationError({
                "seat": (
                    "seat number must be in available range: "
                    f"(1, seats_in_row): (1, {hall.seats_in_row})"
                )
            })

        if Ticket.objects.filter(
            movie_session=self.movie_session,
            row=self.row,
            seat=self.seat,
        ).exists():
            raise ValidationError("Ticket already exists")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_place",
            )
        ]

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )
