from django.db import transaction

from db.models import Order, User, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        new_order = Order(
            user=User.objects.get(username=username)
        )

        if date:
            new_order.created_at = date

        new_order.save()

        session = MovieSession.objects.get(pk=tickets[0].get("movie_session"))

        for ticket in tickets:
            Ticket.objects.create(
                movie_session=session,
                order=new_order,
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
