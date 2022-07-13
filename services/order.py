from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket, MovieSession


def create_order(tickets, username, date=None):
    with transaction.atomic():
        user_id = get_user_model().objects.get(username=username).id
        order = Order.objects.create(user_id=user_id)

        if date:
            order.created_at = date
            order.save()

        for item in tickets:
            movie_session_id = item["movie_session"]
            movie_session = MovieSession.objects.get(id=movie_session_id)

            Ticket.objects.create(
                movie_session=movie_session,
                row=item["row"],
                seat=item["seat"],
                order=order
            )


def get_orders(username=None):
    queryset = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        return queryset.filter(user=user)
    return queryset.order_by("-user__username")
