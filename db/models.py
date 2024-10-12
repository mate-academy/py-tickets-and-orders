from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from django.utils import timezone
from typing import Any


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=255)

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
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


def create_order(tickets: Any, username: Any,
                 date: Any = None) -> None:
    with transaction.atomic():
        user, _ = get_user_model().objects.get_or_create(username=username)
        order = Order.objects.create(
            user=user, created_at=date or timezone.now())

        for ticket_data in tickets:
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=ticket_data["movie_session"],
                order=order
            )


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


class MovieSession(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title}"
                f" {self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:
        if self.row > self.movie_session.cinema_hall.rows or self.row < 1:
            raise ValidationError({"row": [
                f"row number must be in available range:"
                f" (1, rows): (1, {self.movie_session.cinema_hall.rows})"]})
        if (self.seat > self.movie_session.cinema_hall.seats_in_row
                or self.seat < 1):
            raise ValidationError({"seat": [
                f"seat number must be in available range:"
                f" (1, seats_in_row):"
                f" (1, {self.movie_session.cinema_hall.seats_in_row})"]})

    def save(self, *args: str, **kwargs: str) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie_session", "row", "seat"],
                                    name="unique_ticket"),
        ]
