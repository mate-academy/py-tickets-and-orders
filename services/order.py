from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.db import transaction


from db.models import Ticket, Order


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None
                 ) -> QuerySet:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    for ticket in tickets:
        Ticket.objects.create(order=order,
                              movie_session_id=ticket["movie_session"],
                              row=ticket["row"],
                              seat=ticket["seat"]
                              )
    order.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        return orders.filter(user__username=username)
    return orders
