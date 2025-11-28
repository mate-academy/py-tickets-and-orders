from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
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
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie_sessions")
    cinema_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions")
    show_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.movie.title} {self.show_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("movie_session", "row", "seat"), name="unique_ticket")
        ]

    def clean(self):
        # Checa se a row está dentro do limite da sala
        if self.row < 1 or self.row > self.movie_session.cinema_hall.rows:
            raise ValidationError({
                "row": [f"row number must be in available range: (1, rows): (1, {self.movie_session.cinema_hall.rows})"]
            })

        # Checa se o assento está dentro do limite da fila
        if self.seat < 1 or self.seat > self.movie_session.cinema_hall.seats_in_row:
            raise ValidationError({
                "seat": [f"seat number must be in available range: (1, seats_in_row): (1, {self.movie_session.cinema_hall.seats_in_row})"]
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # garante validações antes de salvar
        super().save(*args, **kwargs)

    def __str__(self):
        # Retorna exatamente no formato esperado: "Title YYYY-MM-DD hh:mm:ss (row: X, seat: Y)"
        return f"{self.movie_session.movie.title} {self.movie_session.show_time} (row: {self.row}, seat: {self.seat})"
