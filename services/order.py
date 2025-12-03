from typing import List, Dict, Optional
from django.db import transaction
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from db.models import Order, Ticket, MovieSession
from datetime import datetime


def create_order(
        tickets: List[Dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    user_model = get_user_model()

    user = user_model.objects.get(
        username=username
    )

    order_data = {
        "user": user
    }
    if date is not None:
        order_data["created_at"] = datetime.strptime(
            date,
            "%Y-%m-%d %H:%M"
        )

    with transaction.atomic():
        order = Order.objects.create(
            **order_data
        )

        tickets_to_create = []

        session_map = MovieSession.objects.in_bulk(
            [t["movie_session"] for t in tickets]
        )

        for ticket_data in tickets:
            session_id = ticket_data["movie_session"]
            movie_session = session_map.get(session_id)

            if not movie_session:
                raise MovieSession.DoesNotExist(
                    f"MovieSession with id {session_id} does not exist."
                )

            ticket = Ticket(
                movie_session=movie_session,
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

            ticket.full_clean()

            tickets_to_create.append(
                ticket
            )

        Ticket.objects.bulk_create(
            tickets_to_create
        )

    return order


def get_orders(
        username: Optional[str] = None
) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(
            user__username=username
        )

    return queryset.select_related(
        "user"
    ).prefetch_related(
        "tickets"
    )
