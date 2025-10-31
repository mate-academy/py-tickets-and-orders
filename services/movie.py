from django.db.models import QuerySet, Case, When, IntegerField
from django.db.models.functions import Lower
from django.db import transaction
from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None,
    title: str = None,
) -> QuerySet[Movie]:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    queryset = queryset.distinct()

    # Prioritize titles containing "potter", then the rest alphabetically
    queryset = queryset.annotate(
        is_potter=Case(
            When(title__icontains="potter", then=0),
            default=1,
            output_field=IntegerField()
        ),
        lower_title=Lower("title")
    ).order_by("is_potter", "lower_title")

    return queryset


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )
    if genres_ids:
        movie.genres.set(genres_ids)
    if actors_ids:
        movie.actors.set(actors_ids)

    return movie


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)
