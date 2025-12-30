from datetime import datetime
from db.models import Order, User, Ticket
from django.db.models.query import QuerySet
from django.db import transaction
from services.movie_session import get_movie_session_by_id


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = date
        order.save()

    tickets_list = []
    for ticket in tickets:
        tickets_list.append(
            Ticket(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=get_movie_session_by_id(ticket["movie_session"]),
                order=order,
            )
        )
    Ticket.objects.bulk_create(tickets_list)


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
