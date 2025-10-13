from django.db import transaction
from db.models import Movie

def create_movie(title, description=None, release_date=None):
    with transaction.atomic():
        movie = Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date
        )
    return movie

def get_movies(title=None):
    queryset = Movie.objects.all()
    if title is not None:
        queryset = queryset.filter(title__icontains=title)
    return queryset
