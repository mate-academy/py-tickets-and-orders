class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_ticket_place",
            )
        ]

    def __str__(self) -> str:
        session = self.movie_session
        show_time = session.show_time.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"<Ticket: {session.movie.title} "
            f"{show_time} "
            f"(row: {self.row}, seat: {self.seat})>"
        )

    def clean(self) -> None:
        cinema_hall = self.movie_session.cinema_hall

        if not (1 <= self.row <= cinema_hall.rows):
            msg = (
                "row number must be in available range: "
                f"(1, rows): (1, {cinema_hall.rows})"
            )
            raise ValidationError({"row": [msg]})

        if not (1 <= self.seat <= cinema_hall.seats_in_row):
            msg = (
                "seat number must be in available range: "
                "(1, seats_in_row): "
                f"(1, {cinema_hall.seats_in_row})"
            )
            raise ValidationError({"seat": [msg]})

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
