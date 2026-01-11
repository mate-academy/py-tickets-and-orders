from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])

    session_ids = {ticket["movie_session"] for ticket in tickets}
    session_map = {
        session.id: session
        for session in MovieSession.objects.filter(id__in=session_ids)
    }

    tickets_list = []
    for ticket_data in tickets:
        session_obj = session_map.get(ticket_data["movie_session"])

        tickets_list.append(Ticket(
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=session_obj
        ))

    Ticket.objects.bulk_create(tickets_list)

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
