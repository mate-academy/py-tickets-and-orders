from django.db import transaction

from db.models import Order, User, Ticket, MovieSession


def create_order(tickets: list,
                 username: str,
                 date: str = None
                 ) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                movie_id=ticket["movie_session"]
            )
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
