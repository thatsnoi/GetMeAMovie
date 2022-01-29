import pytest
from pymongo.errors import OperationFailure

from app.db.aggregates import aggregate_filter_movies
from app.models.types import Genre, Platform
from app.models.users import UserMoviesFilter

@pytest.fixture
def filter_data():
    data = {
        'filter': {
            'genres': [Genre.ACTION],
            'minLength': 10,
            'maxLength': 120,
            'platforms': [Platform.NETFLIX],
            'region': 'ES',
            'minAge': 6,
            'maxAge': 18
        }
    }

    model_data = UserMoviesFilter(**data)

    return model_data


def test_aggregate_filter_movies(filter_data):
    response = aggregate_filter_movies(filter_data)

    assert isinstance(response, dict)

    assert 'filteredMovies' in response.keys()
    assert 'maxPages' in response.keys()

    assert len(response['filteredMovies']) > 0
    assert response['maxPages'] > 0


def test_aggregate_filter_movies_no_match(filter_data):
    filter_data.filter.minLength = 1
    filter_data.filter.maxLength = 2

    response = aggregate_filter_movies(filter_data)

    assert len(response['filteredMovies']) == 0
    assert response['maxPages'] == 0


def test_aggregate_filter_movies_invalid_page(filter_data):
    filter_data.page = -1

    with pytest.raises(OperationFailure) as mongo_error:
        aggregate_filter_movies(filter_data)

        assert isinstance(mongo_error, OperationFailure)

