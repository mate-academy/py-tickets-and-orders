from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime


def create_order(tickets, username, date=None):
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)

        for ticket_data in tickets:
            movie_session_id = ticket_data['movie_session']
            row = ticket_data['row']
            seat = ticket_data['seat']

            movie_session = MovieSession.objects.get(id=movie_session_id)

            # Створюємо квиток
            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=row,
                seat=seat
            )

        if date:
            # Конвертуємо рядок дати в об'єкт datetime
            created_at = parse_datetime(date)
            if created_at:
                # Оновлюємо поле created_at
                order.created_at = created_at
                order.save()


def get_orders(username: str = None) -> QuerySet:

    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
