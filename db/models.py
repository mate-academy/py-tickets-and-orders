from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"<Order: {self.created_at}>"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title


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
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (f"<Ticket: {self.movie_session} "
                f"(row: {str(self.order)}, seats: {self.seat})>")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        from services import movie_session  # Import moved here to avoid circular import
        max_rows = movie_session.cinema_hall.rows
        max_seats = movie_session.cinema_hall.seats_in_row
        if self.row < 0 or self.row > max_rows:
            raise ValidationError(f"Rows should be in range [1, {max_rows}], got {self.row}")
        if self.seat < 0 or self.seat > max_seats:
            raise ValidationError(f"Seats should be in range [1, {max_seats}], got {self.seat}")

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['movie_session', 'row', 'seat'],
                name='unique_ticket_per_session'
            ),
        ]
