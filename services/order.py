from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet, Q
from typing import Optional
from datetime import datetime

from db.models import Order, Ticket, MovieSession
from services.user import get_user_by_username


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> Order:
    user = get_user_by_username(username)

    if tickets:
        seat_queries = [
            (Q(movie_session_id=ticket_data["movie_session"])
             & Q(row=ticket_data["row"])
             & Q(seat=ticket_data["seat"]))
            for ticket_data in tickets
        ]
        combined_query = seat_queries[0]
        for query in seat_queries[1:]:
            combined_query |= query

        existing_tickets = Ticket.objects.filter(combined_query)
        if existing_tickets.exists():
            conflict_info = []
            for existing_ticket in existing_tickets:
                conflict_info.append(
                    f"Seat {existing_ticket.row}-{existing_ticket.seat} "
                    f"in session {existing_ticket.movie_session.pk}"
                )
            raise ValueError(
                f"The following seats are already taken: "
                f"{', '.join(conflict_info)}"
            )

    order = Order.objects.create(user=user)

    if date:
        order.created_at = datetime.fromisoformat(date)
        order.save()

    movie_session_ids = {
        ticket_data["movie_session"] for ticket_data in tickets
    }
    movie_sessions = MovieSession.objects.filter(id__in=movie_session_ids)
    movie_session_map = {session.pk: session for session in movie_sessions}

    for ticket_data in tickets:
        movie_session = movie_session_map[ticket_data["movie_session"]]
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_session,
            order=order
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        user = get_user_by_username(username)
        return Order.objects.filter(user=user)
    return Order.objects.all()


def get_order_by_id(order_id: int) -> Order:
    return Order.objects.get(id=order_id)


def get_user_orders(user_id: int) -> QuerySet[Order]:
    return Order.objects.filter(user_id=user_id)
