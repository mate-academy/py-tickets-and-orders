import init_django_orm

from services.movie_session import get_taken_seats

print(get_taken_seats(1))
