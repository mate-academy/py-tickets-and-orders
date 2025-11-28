from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket, MovieSession

User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict], username: str, date=None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)

    if date is not None:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        movie_session_id = ticket_data.pop("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)

        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            **ticket_data
        )

    return order


def get_orders(username: str | None = None):
    query_set = Order.objects.all()

    if username is not None:
        query_set = query_set.filter(user__username=username)

    return query_set
