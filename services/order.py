import datetime

from db.models import Order, User, Ticket
from django.db import transaction


@transaction.atomic
def create_order(tickets: list[int],
                 username: str,
                 date: datetime = None
                 ) -> Order:

    user = User.objects.get(username=username)

    new_order = Order.objects.create(user=user)
    if date is not None:
        new_order.created_at = date
        new_order.save()

    for ticket_data in tickets:
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")
        movie_session = ticket_data.get("movie_session")
        Ticket.objects.create(
            order=new_order,
            row=row,
            seat=seat,
            movie_session_id=movie_session
        )

    return new_order


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
