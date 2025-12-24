from django.db import transaction
import datetime
from db.models import Ticket, Order, User
from django.db.models import QuerySet
from django.contrib.auth import get_user_model


def create_order(
        tickets: list[dict], username: str, date: str = None
) -> None:
    try:
        with transaction.atomic():
            user = get_user_model().objects.get(username=username)

            order_data = {"user": user}
            if date:
                order_data["created_at"] = datetime.datetime.strptime(
                    date, "%Y-%m-%d %H:%M"
                )
            order = Order.objects.create(**order_data)

            ticket_obj = []
            for ticket_date in tickets:
                ticket = Ticket(
                    row=ticket_date["row"],
                    seat=ticket_date["seat"],
                    movie_session_id=ticket_date["movie_session"],
                    order=order
                )
                ticket_obj.append(ticket)
            Ticket.objects.bulk_create(ticket_obj)

    except Exception as e:
        raise e


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
