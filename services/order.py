from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str | None = None
) -> Order | None:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None

    order = Order.objects.create(user=user)

    Order.objects.filter(id=order.id).update(
        created_at=date if date else timezone.now()
    )

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"]
        )
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: str | None = None) -> QuerySet[Order]:
    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user)
        except ObjectDoesNotExist:
            return Order.objects.none()
    return Order.objects.all()
