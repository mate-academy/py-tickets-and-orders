from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> Order:
    new_order = Order(
        user=User.objects.get(username=username)
    )

    if date:
        new_order.created_at = date

    new_order.save()

    session = MovieSession.objects.get(id=tickets[0].get("movie_session"))
    new_tickets = [
        Ticket(
            movie_session=session,
            order=new_order,
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
        for ticket in tickets
    ]

    Ticket.objects.bulk_create(new_tickets)
    return new_order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user=User.objects.get(username=username))

    return Order.objects.all()
