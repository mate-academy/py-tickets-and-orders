from django.db.models import QuerySet
from typing import Optional

from db.models import CinemaHall


def get_cinema_halls() -> QuerySet[CinemaHall]:
    return CinemaHall.objects.all()


def get_cinema_hall_by_id(hall_id: int) -> CinemaHall:
    return CinemaHall.objects.get(id=hall_id)


def create_cinema_hall(
        hall_name: str,
        hall_rows: int,
        hall_seats_in_row: int
) -> CinemaHall:
    if hall_rows <= 0:
        raise ValueError("Rows must be positive")
    if hall_seats_in_row <= 0:
        raise ValueError("Seats per row must be positive")
    
    return CinemaHall.objects.create(
        name=hall_name,
        rows=hall_rows,
        seats_in_row=hall_seats_in_row
    )
