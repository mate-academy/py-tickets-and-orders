from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Ticket:

    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date

    tickets_to_create = []
    for ticket_data in tickets:
        movie_session_id = ticket_data.get("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)
        ticket = Ticket(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        tickets_to_create.append(ticket)
    Ticket.objects.bulk_create(tickets_to_create)

    order.save()
    return order


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
