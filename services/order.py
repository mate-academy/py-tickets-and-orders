from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from db.models import Order, Ticket

User = get_user_model()


@transaction.atomic
def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> None:
    user = User.objects.get(username=username)
    # Criamos a order em um único passo
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    for t_data in tickets:
        Ticket.objects.create(
            order=order,
            row=t_data["row"],
            seat=t_data["seat"],
            movie_session_id=t_data["movie_session"]
        )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
