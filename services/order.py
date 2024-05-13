from typing import List, Dict, Optional
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from datetime import datetime
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: Optional[str] = None
) -> Order:
    try:

        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        for ticket_data in tickets:
            row = ticket_data.get("row")
            seat = ticket_data.get("seat")
            movie_session_id = ticket_data.get("movie_session")

            movie_session = MovieSession.objects.get(id=movie_session_id)

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=row, seat=seat
            )

        return order
    except Exception as e:

        transaction.set_rollback(True)
        raise e


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders
