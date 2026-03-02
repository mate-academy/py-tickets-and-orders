from datetime import datetime
from django.db import transaction
from db.models import Order, User, MovieSession, Ticket


@transaction.atomic
def create_order(
    tickets: list[dict], username: str, date: datetime = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")

    order = Order.objects.create(
        user=user
    )
    if date:
        order.created_at = date
        order.save()

    for ticket in tickets:
        try:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
        except MovieSession.DoesNotExist:
            raise ValueError("Movie session does not exist")

        ticket = Ticket(
            movie_session=movie_session,
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )
        ticket.full_clean()
        ticket.save()

    return order


def get_orders(username: str = None) -> Order:
    queryset = Order.objects.all()
    if username:
        try:
            user = User.objects.get(username=username)
            queryset = queryset.filter(user=user)
        except User.DoesNotExist:
            raise ValueError(
                f"User with username '{username}' does not exist."
            )
    return queryset
