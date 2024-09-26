from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order:
    order = Order.objects.create(
        user=User.objects.get(username=username)
    )

    if date:
        order.created_at = date
        order.save()

    Ticket.objects.bulk_create([
        Ticket(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session=MovieSession.objects.get(
                id=ticket["movie_session"]
            )
        )
        for ticket in tickets
    ])

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
