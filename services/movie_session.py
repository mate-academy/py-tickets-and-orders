from db.models import MovieSession


def get_movie_session(movie_session_id: int) -> MovieSession:
    return MovieSession.objects.get(id=movie_session_id)
