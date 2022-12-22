from db.models import Order


def create_order(
        tickets: list,
        username: str,
        date: str = None
        ):
    pass


def get_orders(username: str = None):
    if username is not None:
        return Order.objects.get(user_id__username=username)
    return Order.objects.all()
