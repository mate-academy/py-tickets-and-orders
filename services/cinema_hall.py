from django.db import transaction
from django.db.models import QuerySet
from db.models import CinemaHall


def get_cinema_halls() -> QuerySet:
    """
    Повертає queryset всіх кінозалів
    """
    return CinemaHall.objects.all()


@transaction.atomic
def create_cinema_hall(
    hall_name: str, hall_rows: int, hall_seats_in_row: int
) -> CinemaHall:
    """
    Створює новий CinemaHall в транзакції
    """
    return CinemaHall.objects.create(
        name=hall_name,
        rows=hall_rows,
        seats_in_row=hall_seats_in_row
    )
