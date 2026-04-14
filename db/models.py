from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from django.conf import settings


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="orders",
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey("MovieSession",
                                      related_name="tickets",
                                      on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order,
                              related_name="tickets",
                              on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie_session",
                                            "row",
                                            "seat"],
                                    name="unique_ticket_place")
        ]

    def __str__(self) -> str:
        show_time = (self.movie_session.show_time.strftime
                     ("%Y-%m-%d %H:%M:%S"))\
            if self.movie_session else ""
        title = self.movie_session.movie.title \
            if self.movie_session else ""
        return (f"{title} {show_time} (row: {self.row}, "
                f"seat: {self.seat})")

    def clean(self) -> None:

        if not self.movie_session:
            return
        hall = self.movie_session.cinema_hall
        errors = {}
        if not (1 <= self.row <= hall.rows):
            errors["row"] = [f"row number must be in "
                             f"available range: (1, rows): "
                             f"(1, {hall.rows})"]
        if not (1 <= self.seat <= hall.seats_in_row):
            errors["seat"] = [f"seat number must be in "
                              f"available range: (1, seats_in_row): "
                              f"(1, {hall.seats_in_row})"]
        if Ticket.objects.filter(movie_session=self.movie_session,
                                 row=self.row,
                                 seat=self.seat).exists():
            raise (ValidationError
                   ({"__all__": ["ticket with such place already exists"]}))
        if errors:
            raise ValidationError(errors)

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
