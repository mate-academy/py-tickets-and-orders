import pytest
from db.models import Genre, Actor, Movie


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def movies_data(db):
    g1 = Genre.objects.create(name="Sci-Fi")
    g2 = Genre.objects.create(name="Action")

    a1 = Actor.objects.create(first_name="Keanu", last_name="Reeves")
    a2 = Actor.objects.create(first_name="Carrie-Anne", last_name="Moss")
    a3 = Actor.objects.create(first_name="Christian", last_name="Bale")

    m1 = Movie.objects.create(title="Matrix", description="First movie")
    m1.genres.set([g1, g2])
    m1.actors.set([a1, a2])

    m2 = Movie.objects.create(title="Matrix 2", description="Second movie")
    m2.genres.set([g1, g2])
    m2.actors.set([a1, a2])

    m3 = Movie.objects.create(title="Batman", description="Dark Knight")
    m3.genres.set([g2])
    m3.actors.set([a3])

    return [m1, m2, m3]
