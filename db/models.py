from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


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
    actors = models.ManyToManyField(to=Actor)
    genres = models.ManyToManyField(to=Genre)

    class Meta:
        indexes = [
            models.Index(fields=["title"], name="title_idx")
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
    show_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    cinema_hall = models.ForeignKey(to=CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(to=MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        pass

    def clean(self):
        rows_range = self.movie_session.cinema_hall.rows
        seats_range = self.movie_session.cinema_hall.seats_in_row
        valid = True
        if not rows_range >= self.row >= 1:
            valid = False
        if not seats_range >= self.seat >= 1:
            valid = False
        if not valid:
            raise ValidationError(f"seat and row must be in range "
                                  f"[1 - {rows_range}] or [1 - {seats_range}]")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (f"{self.movie_session.movie.title}"
                f" {self.movie_session.show_time} (row: {self.row},"
                f" seat: {self.seat})")


class TempoDelete(models.Model):
    field_1 = models.IntegerField()
