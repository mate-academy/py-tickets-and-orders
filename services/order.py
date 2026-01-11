from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from db.models import Order, Ticket, MovieSession, User


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None
                 ) -> Order:
    user = User.objects.get(username=username)
    if date is None:
        order_date = timezone.now().strftime("%Y-%m-%d %H:%M")
    else:
        try:
            # Спочатку читаємо як datetime.date
            date_only = datetime.strptime(date, "%Y-%m-%d").date()
            # Потім перетворюємо на datetime з опівнічним часом
            order_date = datetime.combine(date_only, datetime.time())
        except ValueError:
            try:
                # Якщо формат включає час
                order_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValueError("Date format should be "
                                 "'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM'")
    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=order_date)

        for ticket_data in tickets:
            row = ticket_data["row"]
            seat = ticket_data["seat"]
            movie_session_id = ticket_data["movie_session"]
            movie_session = MovieSession.objects.get(id=movie_session_id)

            Ticket.objects.create(
                order=order,
                row=row,
                seat=seat,
                movie_session=movie_session,
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
