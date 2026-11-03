from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Index, DateTimeField
from django.db.models.constraints import UniqueConstraint
from django.conf import settings


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

    class Meta:
        indexes = [Index(fields=["title"])]

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


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="order")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Orfed: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession,
                                      on_delete=models.CASCADE,
                                      related_name="ticket")
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name="ticket")
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [UniqueConstraint(fields=["row",
                                                "seat",
                                                "movie_session"],
                                        name="unique_place_movie_session")]

    def __str__(self) -> str:
        return (f"Ticket: {self.movie_session.movie} "
                f"{self.movie_session.
                   show_time.strftime('%Y-%m-%d %H:%M:%S')} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:
        ticket_row = self.row
        ticket_seat = self.seat
        if not (1 <= ticket_row <= self.movie_session.
                cinema_hall.rows):
            raise ValidationError({"row": [f"row number must "
                                           f"be in available range: "
                                           f"(1, rows): "
                                           f"(1, {self.movie_session.
                                                  cinema_hall.rows})"]})
        if not (1 <= ticket_seat <= self.movie_session.
                cinema_hall.
                seats_in_row):
            raise ValidationError({"seat":
                                  [f"seat number must be "
                                   f"in available range: "
                                   f"(1, seats_in_row): "
                                   f"(1, {self.movie_session.
                                          cinema_hall.
                                          seats_in_row})"]})

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
