from db.models import Order


def create_order(user) -> Order:
    return Order.objects.create(user=user)


def get_orders_by_user(user):
    return Order.objects.filter(user=user)
