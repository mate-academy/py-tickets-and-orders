from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.db import transaction
from db.models import Ticket, Order, User, MovieSession
from django.core.exceptions import ValidationError


def create_order(tickets: list, username: str, date: str = None) -> Order:
    with transaction.atomic():
        user = get_object_or_404(get_user_model(), username=username)

        order = Order.objects.create(user=user)

        if date:
            try:
                order.created_at = date
                order.save()
            except ValidationError:
                raise ValueError(
                    f"Invalid date format for order creation: {date}"
                )

        for ticket_data in tickets:
            if not MovieSession.objects.filter(
                    id=ticket_data["movie_session"]
            ).exists():
                raise ValueError(
                    f"MS with id {ticket_data['movie_session']} does not exist"
                )

        ticket_objects = [
            Ticket(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
            for ticket_data in tickets
        ]

        Ticket.objects.bulk_create(ticket_objects)

        return order


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        user = get_object_or_404(User, username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
