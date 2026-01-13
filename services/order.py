from django.db import transaction
from datetime import datetime
from db.models import Ticket, Order
from django.contrib.auth import get_user_model


User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> list:
    user = User.objects.get(username=username)
    order = Order.objects.create(
        user=user,
    )
    if date:
        if isinstance(date, str):
            Order.objects.update(
                created_at=datetime.strptime(date, "%Y-%m-%d %H:%M"))
        else:
            Order.objects.update(created_at=date)

    tickets_created = []
    for ticket in tickets:
        tickets_created.append(Ticket.objects.create(
            movie_session_id=ticket.get("movie_session"),
            order=order,
            row=ticket.get("row"),
            seat=ticket.get("seat"),
        ))
    return tickets_created


def get_orders(username: str = None) -> Ticket:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
