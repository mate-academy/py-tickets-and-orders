from django.db import transaction

from db.models import Order, User, Ticket


def create_order(tickets: list[dict], username: str, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)
        if date is not None:
            order = Order.objects.create(user_id=user.id, created_at=date)
            for ticket in tickets:
                Ticket.objects.create(
                    order_id=order.id,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session_id=ticket["movie_session"]
                )
        else:
            order = Order.objects.create(user_id=user.id)
            for ticket in tickets:
                Ticket.objects.create(
                    order_id=order.id,
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session_id=ticket["movie_session"]
                )
    return order


def get_orders(username: str = None):
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user_id=user.id)
    return Order.objects.all().order_by("-user__date_joined")
