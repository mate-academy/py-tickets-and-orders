from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import MovieSession, Order, Ticket

@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date=None,
) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date is not None:
        order.created_at = date
        order.save(update_fields=["created_at"])
    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(id=ticket_data["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )
    return order

def get_orders(username: str = None):
    queryset = Order.objects.all()
    if username is not None:
        queryset = queryset.filter(user__username=username)
    return queryset
