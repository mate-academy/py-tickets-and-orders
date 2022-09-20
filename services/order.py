from datetime import datetime

from django.db import transaction

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict], username, date=None):
    with transaction.atomic():
        order = Order()
        order.user = User.objects.get(username=username)
        order.save()
        if date is not None:
            order.created_at = datetime.strptime(date, '%Y-%m-%d %H:%M')
            order.save()
        for ticket_data in tickets:
            ticket = Ticket.objects.create(
                order=order,
                movie_session=MovieSession.objects.get(
                    id=ticket_data["movie_session"]),
                row=ticket_data["row"],
                seat=ticket_data["seat"])
            ticket.save()
        return order


def get_orders(username=None):
    orders = Order.objects.all().order_by("-id")
    if username is not None:
        orders = orders.filter(user=User.objects.get(username=username).id)
    return orders
