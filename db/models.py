from django import db
from django.db import models
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

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

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

        ordering = ['title']


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


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to="auth.User", on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return f"Order {self.id} by {self.user.username} at {self.created_at}"

    class Meta:
        ordering = ['-created_at']


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, related_name="tickets"
    )

    def clean(self):
        # Validate that the row and seat are within the cinema hall's capacity
        if self.row < 1 or self.row > self.movie_session.cinema_hall.rows:
            raise ValidationError(f"Row {self.row} is out of range"
                                  f"for this cinema hall.")
        if (self.seat < 1 
        or self.seat > self.movie_session.cinema_hall.seats_in_row):
            raise ValidationError(f"Seat {self.seat} is out of range"
                                  f" for this cinema hall.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() before saving
        super().save(*args, **kwargs)   


    class Meta:
        unique_together = ["row", "seat", "movie_session"]

    def __str__(self) -> str:
        return (f"Ticket for {self.movie_session.movie.title} at "
                f"{self.movie_session.show_time}, Row: {self.row},"
                f" Seat: {self.seat}")


class AbstractBaseUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.username

class User(AbstractBaseUser):
    pass

    def __str__(self) -> str:
        return self.username
