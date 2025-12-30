from django.conf import settings
from datetime import date
from django.db import models
from django.contrib.auth.models import (AbstractUser,
                                        PermissionsMixin,
                                        Group,
                                        Permission
                                        )
from django.core.exceptions import ValidationError


class User(AbstractUser, PermissionsMixin):
    date_of_birth = models.DateField(null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        related_name="db_users",
        blank=True,
        help_text=(
            "The groups this user belongs to. "
            "A user will get all permissions granted to each of their groups."
        ),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="db_users_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def __str__(self) -> str:
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField("Actor", related_name="movies")
    genres = models.ManyToManyField("Genre", related_name="movies")
    release_date = models.DateField(default=date.today)

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class CinemaHall(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    cinema_hall = models.ForeignKey(
        CinemaHall,
        on_delete=models.CASCADE,
        related_name="sessions",
    )

    def __str__(self) -> str:
        return f"{self.movie.title} at {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    movie_session = models.ForeignKey(
        "MovieSession", on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_row_seat_movie_session",
            )
        ]

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall
        errors = {}
        if not (1 <= self.row <= hall.rows):
            errors["row"] = [
                f"row number must be in available range:"
                f" (1, rows): (1, {hall.rows})"
            ]
        if not (1 <= self.seat <= hall.seats_in_row):
            errors["seat"] = [
                f"seat number must be in available range:"
                f" (1, seats_in_row): (1, {hall.seats_in_row})"
            ]
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title}"
                f" {self.movie_session.show_time}"
                f" (row: {self.row}, seat: {self.seat})")
