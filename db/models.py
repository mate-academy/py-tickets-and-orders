from django.contrib.auth.models import AbstractUser
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey


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
            models.Index(fields=["title"])
        ]


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
    user = ForeignKey(to="User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title} "
                f"{self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:  # ANN201 fixed
        if not (self.row > 0
                and self.row <= self.movie_session.cinema_hall.rows):
            raise ValidationError({
                "row": "row number must be in available range: (1, rows): "
                f"(1, {self.row - 1})"
            })
        if not (self.seat <= self.movie_session.cinema_hall.seats_in_row
                and self.seat > 0):
            raise ValidationError({
                "seat": "seat number must be in available range:"
                        " (1, seats_in_row): "
                f"(1, {self.seat - 1})"
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        # return super().save(*args, **kwargs)
        try:
            return super().save(*args,
                                **kwargs)
        except IntegrityError as e:
            if "unique_seat_row" in str(e):
                raise ValidationError(
                    {
                        "__all__": "This seat "
                                   "in this row for "
                                   "this session is already taken."}
                )
            raise

    class Meta:
        constraints = [
            models.UniqueConstraint("row", "seat", "movie_session",
                                    name="unique_seat_row")
        ]


class User(AbstractUser):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
