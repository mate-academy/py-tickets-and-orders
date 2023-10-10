from typing import List

from django.db import transaction

import init_django_orm  # noqa: F401

from db.models import MovieSession
from services.movie_session import get_taken_seats
from services.order import create_order, get_orders


def main() -> None:
    # get_taken_seats(1)

    tickets = [
        {
            "row": 6,
            "seat": 12,
            "movie_session": 1
        },
        {
            "row": 6,
            "seat": 13,
            "movie_session": 1
        }
    ]
    # create_order(tickets=tickets, username="Username_1", date="2022-4-20 11:27")
    create_order(tickets=tickets, username="user_1")
    # ttt = get_orders("user1")
    yyy = 0


if __name__ == "__main__":
    main()
