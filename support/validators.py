from typing import Type, Any
from django.db.models.base import Model


def is_value_positive_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 1


def value_positive_int_and_in_range(value: Any,
                                    end: int,
                                    start: int = 1) -> bool:
    return (is_value_positive_int(value)
            and value in range(start, end + 1))


def table_item_exist(model: Type | Model, item_id: int) -> bool:
    return model.objects.filter(id=item_id).exists()
