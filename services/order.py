from django.db import transaction

from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession

from django.contrib.auth import get_user_model

from datetime import datetime

User = get_user_model()


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user, created_at=date_obj)
    else:
        order = Order.objects.create(user=user)
    session_ids = {ticket["movie_session"] for ticket in tickets}
    sessions = MovieSession.objects.in_bulk(session_ids)
    missing_ids = session_ids - sessions.keys()
    if missing_ids:
        raise ValueError(
            f"MovieSession(s) with id(s) {missing_ids} not found."
        )
    ticket_list = [
        Ticket(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=sessions[ticket["movie_session"]],
            order=order
        ) for ticket in tickets
    ]
    Ticket.objects.bulk_create(ticket_list)
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
