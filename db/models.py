from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


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
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{str(self.created_at)}"


class Ticket(models.Model):
    movie_session = models.ForeignKey("MovieSession", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                "row",
                "seat",
                "movie_session"
            ], name="unique_ticket")
        ]

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title} "
                f"{str(self.movie_session.show_time)} (row: {self.row}, "
                f"seat: {self.seat})")

    def clean(self) -> None:
        row = self.row
        max_rows = self.movie_session.cinema_hall.rows
        seat = self.seat
        max_seats = self.movie_session.cinema_hall.seats_in_row
        if not (1 <= row <= max_rows):
            raise ValidationError({"row": ["row number must be in "
                                           "available range: "
                                           f"(1, rows): (1, {max_rows})"]})
        if not (1 <= seat <= max_seats):
            raise ValidationError({"seat": ["seat number must be in "
                                            "available range: "
                                            "(1, seats_in_row): "
                                            f"(1, {max_seats})"]})

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


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
