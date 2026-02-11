from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

# =====================
# 1. Custom User
# =====================
class User(AbstractUser):
    pass


# =====================
# 2. Genre
# =====================
class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# =====================
# 3. Actor
# =====================
class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# =====================
# 4. Movie
# =====================
class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(default=0)
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    def __str__(self):
        return self.title


# =====================
# 5. CinemaHall
# =====================
class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


# =====================
# 6. MovieSession
# =====================
class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self):
        return f"{self.movie.title} {self.show_time}"


# =====================
# 7. Order
# =====================
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"<Order: {self.created_at}>"


# =====================
# 8. Ticket
# =====================
class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"], name="unique_ticket"
            )
        ]

    def __str__(self):
        return f"<Ticket: {self.movie_session.movie.title} {self.movie_session.show_time} (row: {self.row}, seat: {self.seat})>"

    def clean(self):
        hall = self.movie_session.cinema_hall
        errors = {}
        if self.row < 1 or self.row > hall.rows:
            errors["row"] = f"row number must be in available range: (1, rows): (1, {hall.rows})"
        if self.seat < 1 or self.seat > hall.seats_in_row:
            errors["seat"] = f"seat number must be in available range: (1, seats_in_row): (1, {hall.seats_in_row})"
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()  # виклик clean перед збереженням
        super().save(*args, **kwargs)
