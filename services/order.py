import datetime

from django.db import transaction

from db.models import Order, User, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = datetime.datetime.strptime(
                date, "%Y-%m-%d %H:%M")
        for ticket_data in tickets:
            Ticket.objects.\
                create(order=order,
                       movie_session_id=ticket_data["movie_session"],
                       row=ticket_data["row"],
                       seat=ticket_data["seat"])
        order.save()
        return order


def get_orders(username: str = None) -> list:
    if username:
        return Order.objects.filter(user__username=username).values_list()
    return Order.objects.values_list()
