from django.core.exceptions import ValidationError

class Ticket(models.Model):
    movie_session = models.ForeignKey("MovieSession", on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="unique_ticket_for_session"
            )
        ]

    def __str__(self):
        return f"<Ticket: {self.movie_session.movie.title} {self.movie_session.show_time} (row: {self.row}, seat: {self.seat})>"

    def clean(self):
        hall = self.movie_session.cinema_hall
        errors = {}
        if self.row > hall.rows or self.row < 1:
            errors["row"] = [f"row number must be in available range: (1, rows): (1, {hall.rows})"]
        if self.seat > hall.seats_in_row or self.seat < 1:
            errors["seat"] = [f"seat number must be in available range: (1, seats_in_row): (1, {hall.seats_in_row})"]
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
