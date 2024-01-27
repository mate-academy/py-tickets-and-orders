from django.db.models import QuerySet
from db.models import CinemaHall, Ticket, MovieSession, Order
import datetime
import init_django_orm

def get_cinema_halls() -> QuerySet:
    return CinemaHall.objects.all()


def create_cinema_hall(
        hall_name: str, hall_rows: int, hall_seats_in_row: int
) -> CinemaHall:
    return CinemaHall.objects.create(
        name=hall_name, rows=hall_rows, seats_in_row=hall_seats_in_row
    )


if __name__ == '__main__':
    cinema_hall = CinemaHall.objects.create(name="Blue", rows=18, seats_in_row=24)
    movie_session = MovieSession.objects.create(
        show_time=datetime.datetime(2022, 3, 20, 19, 30),
        movie_id=1,
        cinema_hall=cinema_hall)

