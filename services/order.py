from db.models import Order


def create_order(
        tickets: list[dict],
        username: str,
        date: None
):
    pass


def get_orders(username: str = None):
    if username:
        Order.objects.filter(user__username__exact=username)
    return Order.objects.all()
