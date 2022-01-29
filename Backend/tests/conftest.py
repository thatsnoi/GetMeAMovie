import pytest

from app.db.db_session import database_instance
from app.recommenders.Recommender import recommender

@pytest.fixture(autouse=True, scope='session')
def database_create_connection(request):
    database_instance.create_connection()

    def database_close_connection():
        database_instance.close_connection()
    
    request.addfinalizer(database_close_connection)

    return database_instance


@pytest.fixture(autouse=True, scope='session')
def recommender_load_model():
    recommender.load_model()
