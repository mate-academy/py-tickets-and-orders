from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Index, UniqueConstraint


class Genre(models.Model):
    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            Index(fields=["title"])
        ]


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall
        if self.row > hall.rows:
            raise ValidationError({
                "row": (
                    f"row number must be in available range: "
                    f"(1, rows): (1, {hall.rows})"
                )
            })
        if self.seat > hall.seats_in_row:
            raise ValidationError({
                "seat": (
                    f"seat number must be in available range: "
                    f"(1, seats_in_row): (1, {hall.seats_in_row})"
                )
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket"
            )
        ]
