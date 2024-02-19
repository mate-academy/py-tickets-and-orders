import init_django_orm  # noqa: F401

import datetime

from db.models import CinemaHall, MovieSession, Order, Ticket


def main() -> None:
    cinema_hall = CinemaHall.objects.create(name="Blue", rows=18, seats_in_row=24)
    movie_session = MovieSession.objects.create(
        show_time=datetime.datetime(2022, 3, 20, 19, 30),
        movie_id=1,
        cinema_hall=cinema_hall,
    )
    order = Order.objects.create(user_id=1)

    ticket = Ticket.objects.create(
        movie_session=movie_session, order=order, row=19, seat=20
    )
    ticket.clean()

    # ticket = Ticket.objects.create(
    #     movie_session=movie_session,
    #     order=order,
    #     row=17,
    #     seat=26
    # )
    # ticket.clean()


if __name__ == "__main__":
    main()
