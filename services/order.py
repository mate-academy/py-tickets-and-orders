from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets, username, date=None):
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


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.order_by("-user")
