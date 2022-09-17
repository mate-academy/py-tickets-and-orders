from django.db import transaction

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets: list, username: str,
                 date=None):
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"]
        )


def get_orders(username: str = None):
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)
    return orders
