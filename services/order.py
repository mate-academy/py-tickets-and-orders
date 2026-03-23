from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.contrib.auth import get_user_model
from datetime import datetime
from django.db.models import QuerySet


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = get_user_model().objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        Order.objects.filter(id=order.id).update(created_at=parsed_date)

    ticket_objs = []
    session_ids = {item["movie_session"] for item in tickets}
    existing_sessions = set(
        MovieSession.objects.filter(
            id__in=session_ids).values_list("id", flat=True)
    )

    for item in tickets:
        if item["movie_session"] not in existing_sessions:
            raise Exception(
                f"MovieSession {item['movie_session']} does not exist"
            )

        ticket = Ticket(
            row=item["row"],
            seat=item["seat"],
            order=order,
            movie_session_id=item["movie_session"]
        )

        ticket.full_clean()

        ticket_objs.append(ticket)

    Ticket.objects.bulk_create(ticket_objs)

    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
