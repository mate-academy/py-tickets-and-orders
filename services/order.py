from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from django.core.exceptions import ObjectDoesNotExist, ValidationError


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(
            f"User with username '{username}' does not exist.")

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order = Order.objects.create(user=user, created_at=created_at)
    else:
        order = Order.objects.create(user=user)

    ticket_objects = []
    for ticket in tickets:
        if not MovieSession.objects.filter(
                id=ticket["movie_session"]).exists():
            raise ValidationError(
                f"MovieSession with id "
                f"{ticket['movie_session']} does not exist.")

        ticket_instance = Ticket(
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
            movie_session_id=ticket["movie_session"]
        )
        ticket_instance.full_clean()
        ticket_objects.append(ticket_instance)
    Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> list[Order]:
    queryset = Order.objects.select_related("user").order_by("-created_at")
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
