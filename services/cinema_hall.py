from django.db.models import QuerySet

from db.models import CinemaHall


def get_cinema_halls() -> QuerySet[CinemaHall]:
    return CinemaHall.objects.all()


def get_cinema_hall_by_id(hall_id: int) -> CinemaHall:
    return CinemaHall.objects.get(id=hall_id)


def create_cinema_hall(
        name: str,
        rows: int,
        seats_in_row: int
) -> CinemaHall:
    if rows <= 0:
        raise ValueError("Rows must be positive")
    if seats_in_row <= 0:
        raise ValueError("Seats per row must be positive")

    return CinemaHall.objects.create(
        name=name,
        rows=rows,
        seats_in_row=seats_in_row
    )
