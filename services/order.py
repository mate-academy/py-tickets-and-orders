from django.db import transaction
from db.models import MovieSession, Order, Ticket, User


def create_order(tickets: list, username: str, date: str = None) -> None:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session_id = ticket["movie_session"]
            movie_session = MovieSession.objects.get(id=movie_session_id)
            Ticket.objects.create(movie_session=movie_session,
                                  order=order, row=row, seat=seat)


def get_orders(username: str = None) -> list:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
