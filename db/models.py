from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# --------------------
# Modelo User personalizado
# --------------------
class User(AbstractUser):
    pass

# --------------------
# Modelo Movie
# --------------------
class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)  # índice adicionado
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

# --------------------
# Modelo Order
# --------------------
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"<Order: {self.created_at}>"

# --------------------
# Modelo Ticket
# --------------------
class Ticket(models.Model):
    movie_session = models.ForeignKey('MovieSession', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['movie_session', 'row', 'seat'],
                name='unique_ticket_per_seat_session'
            )
        ]

    def clean(self):
        errors = {}
        if self.row < 1 or self.row > self.movie_session.cinema_hall.rows:
            errors['row'] = [f'row number must be in available range: (1, rows): (1, {self.movie_session.cinema_hall.rows})']
        if self.seat < 1 or self.seat > self.movie_session.cinema_hall.seats_in_row:
            errors['seat'] = [f'seat number must be in available range: (1, seats_in_row): (1, {self.movie_session.cinema_hall.seats_in_row})']
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"<Ticket: {self.movie_session.movie.title} {self.movie_session.show_time} (row: {self.row}, seat: {self.seat})>"
