from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


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
    description = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)

    def __str__(self) -> str:
        return self.title


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (
            f"{self.movie.title} at "
            f"{self.show_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_per_session",
            )
        ]

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall

        if not (1 <= self.row <= hall.rows):
            raise ValidationError(
                {
                    "row": [
                        (
                            "row number must be in available range: "
                            f"(1, rows): (1, {hall.rows})"
                        )
                    ]
                }
            )

        if not (1 <= self.seat <= hall.seats_in_row):
            raise ValidationError(
                {
                    "seat": [
                        (
                            "seat number must be in available range: "
                            f"(1, seats_in_row): (1, {hall.seats_in_row})"
                        )
                    ]
                }
            )

        if (
            Ticket.objects.filter(
                movie_session=self.movie_session,
                row=self.row,
                seat=self.seat,
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                {
                    "seat": [
                        "ticket for this seat already exists for this session"
                    ]
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        show_time = self.movie_session.show_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        title = self.movie_session.movie.title
        return f"{title} {show_time} (row: {self.row}, seat: {self.seat})"
