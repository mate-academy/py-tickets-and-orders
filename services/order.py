# services/order.py
from db.models import Order, Ticket, MovieSession
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()

@transaction.atomic
def create_order(tickets, username, date=None):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User {username} does not exist.")

    created_at = date if date else timezone.now()
    order = Order.objects.create(user=user, created_at=created_at)

    for t in tickets:
        movie_session = MovieSession.objects.get(id=t["movie_session"])
        ticket = Ticket(
            movie_session=movie_session,
            order=order,
            row=t["row"],
            seat=t["seat"],
        )
        ticket.save()
    return order

def get_orders(username=None):
    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs