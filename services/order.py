from django.db import transaction

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    order = Order(user=user)
    order.save()
    if date is not None:
        order.created_at = date
        order.save()

    for ticket in tickets:
        Ticket.objects.create(
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"],
            order=order
        )


def get_orders(username: str = None):
    orders = Order.objects.all().order_by("-user__id")
    if username is not None:
        orders = orders.filter(user__username=username)
    return orders.values_list()
