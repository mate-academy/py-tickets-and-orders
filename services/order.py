from django.db.models import QuerySet

from django.contrib.auth import get_user_model

from db.models import Order, Ticket

from django.db import transaction

from datetime import datetime


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> None:
    # Creating tickets
    with transaction.atomic():
        # Get user id by username
        user_instance = get_user_model().objects.get(username=username)
        # Create Order
        order = Order.objects.create(user=user_instance)
        # If date presented, update it
        if date:
            parsed_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = parsed_date
            order.save(update_fields=["created_at"])
        # Prepairing tickets data for adding to DB
        ticket_instances = []
        for ticket_data in tickets:
            ticket = Ticket(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order=order
            )
            ticket.full_clean()
            ticket_instances.append(ticket)
        # Add tickets into DB
        Ticket.objects.bulk_create(ticket_instances)


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        return queryset.filter(user__username=username)
    return queryset
