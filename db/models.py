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


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

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
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"Order: {self.created_at.strftime('%d/%m/%Y %H:%M:%S')}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(to=MovieSession, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(to=Order, on_delete=models.DO_NOTHING)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (f"Ticket: "
                f"{self.movie_session.movie.title} "
                f"{self.order.created_at.strftime('%d/%m/%Y %H:%M:%S')}"
                f"(row: {self.row}, seat: {self.seat})")


    class Meta:
        constraints = [UniqueConstraint(fields=["row", "seat", "movie_session"], name="unique_ticket")]


    def clean(self) -> None:
        if not (1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row):
            raise ValidationError(
                {"seat": f"Seat must be between 1 and "
                         f"{self.movie_session.cinema_hall.seats_in_row}, not {self.seat}"
                 }
            )
        if not (1 <= self.row <= self.movie_session.cinema_hall.rows):
            raise ValidationError(
                {"row": f"Row must be between 1 and "
                        f"{self.movie_session.cinema_hall.rows}, not {self.row}"
                 }
            )


    def save(self, *args, **kwargs) -> None:
        super.full_clean()
        return super().save(*args, **kwargs)
