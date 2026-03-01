from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self,
                    username: str,
                    password: str,
                    **extra_fields) -> User:

        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         username: str,
                         password: str,
                         **extra_fields) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    actors = models.ManyToManyField("Actor")

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey("MovieSession", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket"
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        hall = self.movie_session.cinema_hall
        if self.row < 1 or self.row > hall.rows:
            raise ValidationError({
                "row": (
                    f"Row number must be in available range: "
                    f"(1, rows): (1, {hall.rows})"
                )
            })
        if self.seat < 1 or self.seat > hall.seats_in_row:
            raise ValidationError({
                "seat": (
                    f"Seat number must be in available range: "
                    f"(1, seats_in_row): (1, {hall.seats_in_row})"
                )
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    cinema_hall = models.ForeignKey("CinemaHall", on_delete=models.CASCADE)


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
