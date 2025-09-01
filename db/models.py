from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    """Custom User model."""
    pass

class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title

class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class MovieSession(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} {self.show_time}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"<Order: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}>"

class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_per_session_row_seat",
            )
        ]

    def __str__(self):
        return (
            f"<Ticket: {self.movie_session.movie.title} "
            f"{self.movie_session.show_time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"(row: {self.row}, seat: {self.seat})>"
        )

    def clean(self):
        hall = self.movie_session.cinema_hall
        errors = {}
        if not (1 <= self.row <= hall.rows):
            errors["row"] = [
                f"row number must be in available range: (1, rows): (1, {hall.rows})"
            ]
        if not (1 <= self.seat <= hall.seats_in_row):
            errors["seat"] = [
                f"seat number must be in available range: (1, seats_in_row): (1, {hall.seats_in_row})"
            ]
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)