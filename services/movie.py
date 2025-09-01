# services/movie.py
from db.models import Movie
from django.db import transaction

def get_movies(title=None):
    qs = Movie.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    return qs

@transaction.atomic
def create_movie(title, description=None, duration=None):
    movie = Movie(title=title, description=description, duration=duration)
    movie.save()
    return movie