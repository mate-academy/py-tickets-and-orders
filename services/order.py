from django.db import transaction
from db.models import Order, Ticket, User


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        for ticket in tickets:
            if date:
                new_order.created_at = date
                new_order.save()
            Ticket.objects.create(seat=ticket.get("seat"),
                                  row=ticket.get("row"),
                                  movie_session_id=ticket.get("movie_session"),
                                  order=new_order)


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
