from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    pass

class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    # остальные существующие поля Movie оставь как были


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        "MovieSession",
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket",
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        if self.row < 1 or self.row > self.movie_session.cinema_hall.rows:
            raise ValidationError({
                "row": (
                    "row number must be in available range: "
                    f"(1, rows): (1, {self.movie_session.cinema_hall.rows})"
                )
            })

        if (
                self.seat < 1
                or self.seat > self.movie_session.cinema_hall.seats_in_row
        ):
            raise ValidationError({
                "seat": (
                    "seat number must be in available range: "
                    "(1, seats_in_row): "
                    f"(1, {self.movie_session.cinema_hall.seats_in_row})"
                )
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
