from db.models import Ticket


def create_ticket(order, movie_session, row, seat) -> Ticket:
    return Ticket.objects.create(
        order=order,
        movie_session=movie_session,
        row=row,
        seat=seat
    )


def update_ticket(ticket_id, movie_session=None, row=None, seat=None):
    ticket = Ticket.objects.get(id=ticket_id)
    if movie_session:
        ticket.movie_session = movie_session
    if row:
        ticket.row = row
    if seat:
        ticket.seat = seat
    ticket.save()


def delete_ticket(ticket_id: int):
    Ticket.objects.get(id=ticket_id).delete()


def get_tickets_by_user(user):
    return Ticket.objects.filter(order__user=user)
