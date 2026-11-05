from db.models import Order


def create_order(user_id: int) -> Order:
    order = Order.objects.create(user_id=user_id)
    return order

def get_order_by_id(order_id: int) -> Order:
    return Order.objects.get(id=order_id)
