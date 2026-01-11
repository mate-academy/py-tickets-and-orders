from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.core.exceptions import ValidationError



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
        return f"{self.movie.title} {self.show_time.strftime('%Y-%m-%d %H:%M:%S')}"


# class User(AbstractUser):
#     pass
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    objects = UserManager()

    def __str__(self):
        return self.username

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"<Order: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}>"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_seat_for_session"
            )
        ]

    def __str__(self) -> str:
        session_time_str = self.movie_session.show_time.strftime('%Y-%m-%d %H:%M:%S')
        return (f"<Ticket: {self.movie_session.movie.title} {session_time_str} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self):
        super().clean()

        cinema_hall = self.movie_session.cinema_hall
        errors = {}

        if not (1 <= self.row <= cinema_hall.rows):
            errors["row"] = [
                f"row number must be in available range: (1, {cinema_hall.rows})"
            ]

        if not (1 <= self.seat <= cinema_hall.seats_in_row):
            errors["seat"] = [
                f"seat number must be in available range: (1, {cinema_hall.seats_in_row})"
            ]

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)