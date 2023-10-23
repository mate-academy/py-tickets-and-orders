import init_django_orm # noqa 401

from services.movie_session import get_taken_seats


print(get_taken_seats(4))