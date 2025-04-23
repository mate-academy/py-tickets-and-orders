from datetime import datetime
from django.db.models import QuerySet
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = None
        if date:
            order = Order.objects.create(
                user=User.objects.get(username=username),
                created_at=datetime.strptime(date, "%Y-%m-%d %H:%M")
            )
        else:
            order = Order.objects.create(
                user=User.objects.get(username=username),
            )

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.save()

        tickets = [Ticket(
            movie_session=MovieSession.objects.get(id=t.get("movie_session")),
            order=order,
            row=t.get("row"),
            seat=t.get("seat")
        ) for t in tickets]
        Ticket.objects.bulk_create(tickets)


def get_orders(
        username: str = None
) -> QuerySet :
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
