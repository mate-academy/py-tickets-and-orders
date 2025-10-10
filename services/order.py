from db.models import Order, Ticket, User
from django.db import transaction

@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str | None = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save(update_fields=["created_at"])
    ticket_objects = [
        Ticket(
            movie_session=Ticket.objects.get(
                movie_session__id=ticket["movie_session"]
            ).movie_session,
            row=ticket["row"],
            seat=ticket["seat"],
            order=order,
        )
        for ticket in tickets
    ]
    Ticket.objects.bulk_create(ticket_objects)
    return order


def get_orders(username: str = None) -> list[Order]:
    if username:
        return list(Order.objects.filter(user__username=username).prefetch_related("tickets"))
    return list(Order.objects.all().prefetch_related("tickets"))
