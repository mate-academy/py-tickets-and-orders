from django.db import transaction

from datetime import datetime

from db.models import Order, User, Ticket


def create_order(
        tickets: list,
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            date_time = datetime.strptime(
                date,
                "%Y-%m-%d %H:%M"
            )
            order.created_at = date_time
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"]
            )
    return order


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
