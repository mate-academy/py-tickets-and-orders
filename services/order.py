from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from db.models import Order, Ticket, MovieSession
from django.db import transaction

User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: None) -> Order:
    if not tickets:
        raise ValueError("Tickets list cannot be empty")

    user = User.objects.get(username=username)

    order = Order(user=user)
    if date:
        order.created_at = date
    order.save()

    for ticket_data in tickets:
        movie_session = ticket_data["movie_session"]
        if isinstance(movie_session, int):
            movie_session = MovieSession.objects.get(id=movie_session)

        ticket = Ticket(
            order=order,
            movie_session=movie_session,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )
        ticket.save()

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all().order_by("-created_at")
    if username:
        orders = orders.filter(user__username=username)
    return orders
