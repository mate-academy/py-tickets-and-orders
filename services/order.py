from django.db import transaction

from db.models import User, Order, Ticket


def create_order(tickets: list[dict], username: str, date: str = None):
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(username=username)
        )
        if date:
            new_order.created_at = date
        new_order.save()

        for ticket_info in tickets:
            Ticket.objects.create(
                order=new_order,
                movie_session_id=ticket_info["movie_session"],
                row=ticket_info["row"],
                seat=ticket_info["seat"]
            )
        return new_order


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
