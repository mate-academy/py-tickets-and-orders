from django.utils import timezone
from db.models import User, Ticket, Order, MovieSession
from typing import Optional
from django.db import transaction
from datetime import datetime


def create_order(*, username, tickets, date=None):
    if not tickets:
        raise ValueError("Список квитків не може бути порожнім.")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"Користувач з ім'ям '{username}' не знайдений.")

    created_at = datetime.strptime(date, "%Y-%m-%d %H:%M") if date else timezone.now()

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=created_at)

        for ticket_data in tickets:
            try:
                movie_session = MovieSession.objects.get(id=ticket_data['movie_session'])
            except MovieSession.DoesNotExist:
                raise ValueError(f"Сеанс фільму з ID {ticket_data['movie_session']} не знайдено.")

            Ticket.objects.create(
                row=ticket_data['row'],
                seat=ticket_data['seat'],
                movie_session=movie_session,  # Правильний тип даних
                order=order
            )

    return order




def get_orders(username: Optional[str] = None) -> list[Order]:
    if username:
        if not User.objects.filter(username=username).exists():
            raise ValueError(f"User with username '{username}' does not exist.")
        return Order.objects.filter(user__username=username)

    return Order.objects.all()
