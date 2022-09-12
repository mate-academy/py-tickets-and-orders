from django.db import transaction


from db.models import Order, Ticket, User


def create_order(tickets, username, date=None):
    with transaction.atomic():
        order = Order.objects.create(user=User.objects.get(username=username))
        if date:
            Order.objects.update(created_at=date)

        for ticket in tickets:
            Ticket.objects.create(movie_session_id=ticket["movie_session"],
                                  order=order,
                                  row=ticket["row"],
                                  seat=ticket["seat"])

        return order


def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all().order_by("-user__username")
