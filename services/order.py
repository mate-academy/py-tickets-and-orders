from django.db import transaction
from django.contrib.auth import get_user_model
from database_app.models import Order, Ticket, MovieSession
from datetime import datetime

User = get_user_model()


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    try:
        user_instance = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")

    order_kwargs = {"user": user_instance}

    if date:
        parsed_date = None
        possible_formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
        for fmt in possible_formats:
            try:
                parsed_date = datetime.strptime(date, fmt)
                break
            except ValueError:
                continue
        if parsed_date is None:
            raise ValueError(
                f"Invalid date format: {date}. "
                f"Please use 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD HH:MM'."
            )

        order_kwargs["created_at"] = parsed_date


    current_order = Order.objects.create(**order_kwargs)

    tickets_to_create_instances = []
    for ticket_data in tickets:
        movie_session_id = ticket_data.get("movie_session")
        row = ticket_data.get("row")
        seat = ticket_data.get("seat")

        if movie_session_id is None or row is None or seat is None:
            raise ValueError(
                "Each ticket dictionary must contain 'movie_session', 'row', and 'seat' keys."
            )

        try:
            movie_session_instance = MovieSession.objects.get(id=movie_session_id)
        except MovieSession.DoesNotExist:
            raise ValueError(f"MovieSession with id {movie_session_id} does not exist.")


        ticket_instance = Ticket(
            order=current_order,
            movie_session=movie_session_instance,
            row=row,
            seat=seat
        )
        tickets_to_create_instances.append(ticket_instance)


    for ticket in tickets_to_create_instances:
        ticket.clean()

    Ticket.objects.bulk_create(tickets_to_create_instances)

    return current_order


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()