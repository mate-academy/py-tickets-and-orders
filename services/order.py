from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from db.models import Order, Ticket, MovieSession

User = get_user_model()


def create_order(tickets: list[dict], username: str, date: str = None) -> Order:

    with transaction.atomic():
        user = User.objects.get(username=username)

        order_data = {"user": user}
        if date:
            parsed_date = parse_datetime(date)
            if not parsed_date:
                raise ValueError("Invalid date format. Use 'YYYY-MM-DD HH:MM'.")
            order_data["created_at"] = parsed_date

        order = Order.objects.create(**order_data)

        tickets_objs = []
        for ticket_data in tickets:
            tickets_objs.append(
                Ticket(
                    order=order,
                    movie_session=MovieSession.objects.get(pk=ticket_data["movie_session"]),
                    row=ticket_data["row"],
                    seat=ticket_data["seat"]
                )
            )

        Ticket.objects.bulk_create(tickets_objs)
        return order


def get_orders(username: str = None) -> QuerySet[Order]:

    qs = Order.objects.all()
    if username:
        qs = qs.filter(user__username=username)
    return qs
