from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# ---------------------------
# Custom User
# ---------------------------
class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="db_user_groups",
        blank=True,
        help_text=(
            "The groups this user belongs to. "
            "A user will get all permissions granted to each of their groups."
        ),
        related_query_name="db_user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="db_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="db_user",
    )


# ---------------------------
# Genre
# ---------------------------
class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


# ---------------------------
# Actor
# ---------------------------
class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


# ---------------------------
# CinemaHall
# ---------------------------
class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return self.name


# ---------------------------
# Movie
# ---------------------------
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duração em minutos")
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")

    class Meta:
        indexes = [models.Index(fields=["title"])]

    def __str__(self) -> str:
        return self.title


# ---------------------------
# MovieSession
# ---------------------------
class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="sessions"
    )
    cinema_hall = models.ForeignKey(
        CinemaHall, on_delete=models.CASCADE, related_name="sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} - {self.show_time}"


# ---------------------------
# Order
# ---------------------------
class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Order: {self.created_at}>"


# ---------------------------
# Ticket
# ---------------------------
class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket",
            )
        ]

    def clean(self) -> None:
        errors = {}
        if self.row < 1 or self.row > self.movie_session.cinema_hall.rows:
            errors["row"] = [
                f"row number must be in available range: (1, rows): "
                f"(1, {self.movie_session.cinema_hall.rows})"
            ]
        if (
            self.seat < 1
            or self.seat > self.movie_session.cinema_hall.seats_in_row
        ):
            errors["seat"] = [
                f"seat number must be in available range: "
                f"(1, seats_in_row): "
                f"(1, {self.movie_session.cinema_hall.seats_in_row})"
            ]

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"<Ticket: {self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})>"
        )
