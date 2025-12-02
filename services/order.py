from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from typing import Optional


User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order | None:

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    with transaction.atomic():

        order = Order.objects.create(user=user)

        if date:
            parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            Order.objects.filter(id=order.id).update(created_at=parsed_date)
            order.refresh_from_db()

        for ticket_dict in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_dict["movie_session"]
            )

            ticket_obj = Ticket(
                row=ticket_dict["row"],
                seat=ticket_dict["seat"],
                movie_session=movie_session,
                order=order
            )
            ticket_obj.full_clean()
            ticket_obj.save()

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:

    if username:
        try:
            user = User.objects.get(username=username)
            return Order.objects.filter(user=user).order_by("-created_at")
        except User.DoesNotExist:
            return Order.objects.none()
    else:
        return Order.objects.all().order_by("-created_at")
