from django.db.models import QuerySet
from django.db import transaction
from db.models import MovieSession, Order, User, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: str | None = None) -> Order:
    with transaction.atomic():
        user, _ = User.objects.get_or_create(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        #  Fix the Failed: DID NOT RAISE <class 'Exception'> pytest error
        movie_session_ids = {ticket["movie_session"] for ticket in tickets}
        existing_ids = set(
            MovieSession.objects.filter(id__in=movie_session_ids)
            .values_list("id", flat=True)
        )

        missing_ids = movie_session_ids - existing_ids
        if missing_ids:
            raise ValueError(f"Invalid movie_session IDs: {missing_ids}")

        tickets_to_create = [
            Ticket(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(tickets_to_create)

        return order


def get_orders(username: str | None = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
