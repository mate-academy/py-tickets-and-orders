from db.models import Movie


def get_movies(title: str = None) -> list[Movie]:
    if title:
        return list(Movie.objects.filter(title__icontains=title))
    return list(Movie.objects.all())
