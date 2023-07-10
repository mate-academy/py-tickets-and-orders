from django.contrib.auth import get_user_model
from db.models import MovieSession, Ticket, Order
from django.db import transaction
from django.db.models import QuerySet


def validate_movie_session(movie_session_id: int) -> bool:
    try:
        MovieSession.objects.get(id=movie_session_id)
    except MovieSession.DoesNotExist:
        raise MovieSession.DoesNotExist(
            f"MovieSession with id: {movie_session_id}, does not exist"
        )

    return True


def create_order(
        tickets: list[Ticket],
        username: str,
        date: str = None
) -> None:

    current_user = get_user_model().objects.get(username=username)
    order = Order(user=current_user)

    for ticket in tickets:
        validate_movie_session(ticket["movie_session"])
        movie = MovieSession.objects.get(id=ticket["movie_session"])

        if date:
            order.created_at = date

        with transaction.atomic():
            order.save()

            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie,
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()

    if username:
        orders = orders.filter(user__username=username)

    return orders
