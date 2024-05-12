from typing import Any

import init_django_orm  # noqa: F401

from services import cinema_hall


def main() -> Any:
    return cinema_hall.create_cinema_hall(
        "new_hall",
        25,
        25
    )


if __name__ == "__main__":
    print(main())
