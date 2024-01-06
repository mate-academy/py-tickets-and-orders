from django.db import transaction
from django.db.models import QuerySet


from db.models import Order, Ticket, User
from services import movie_session


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=movie_session.get_movie_session_by_id(
                    ticket.get("movie_session")
                ),
                order=order,
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all().values_list("user__username")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
