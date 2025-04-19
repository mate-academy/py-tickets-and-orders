from db.models import Ticket, Order

# Пример функции для создания билета
def create_ticket(user, order, movie_session, price):
    return Ticket.objects.create(
        user=user,
        order=order,
        movie_session=movie_session,
        price=price
    )

# Пример функции для получения всех билетов для пользователя
def get_tickets_by_user(user):
    return Ticket.objects.filter(user=user)

# Пример функции для обновления информации о билете
def update_ticket(ticket_id, price=None, movie_session=None):
    ticket = Ticket.objects.get(id=ticket_id)
    if price:
        ticket.price = price
    if movie_session:
        ticket.movie_session = movie_session
    ticket.save()
    return ticket
