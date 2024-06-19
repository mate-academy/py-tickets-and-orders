from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        tickets_objects = []
        for ticket in tickets:
            temp = (Ticket.objects
                    .create(seat=ticket["seat"],
                            row=ticket["row"],
                            movie_session_id=ticket["movie_session"],
                            order=order))
            tickets_objects.append(temp)

        order.tickets.set(tickets_objects)
        if date:
            order.created_at = date
        order.save()


def get_orders(username: str = None) -> QuerySet[Order]:
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)
    return query
