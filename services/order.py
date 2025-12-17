from typing import List
from datetime import datetime
from db.models import Ticket, User, Order, MovieSession
from django.db import transaction
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str,
                 date: datetime = None
                 ) -> List[Ticket]:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()
    created_tickets = []

    for ticket_dic in tickets:

        row = ticket_dic.get("row")
        seat = ticket_dic.get("seat")
        movie_session_id = ticket_dic.get("movie_session")

        try:
            movie_session = MovieSession.objects.get(id=movie_session_id)

        except Exception as e:
            print(f"Other exception occurred: {type(e).__name__} - {e}")

        ticket = Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=row,
            seat=seat
        )
        created_tickets.append(ticket)

    return created_tickets


def get_orders(username: str = None) -> QuerySet :
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
