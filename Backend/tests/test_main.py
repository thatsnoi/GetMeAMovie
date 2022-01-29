import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.types import Genre, Platform

client = TestClient(app)

@pytest.fixture
def filter_data():
    data = {
        'filter': {
            'genres': [Genre.ACTION, Genre.COMEDY],
            'minLength': 0,
            'maxLength': 200,
            'platforms': [Platform.NETFLIX, Platform.PRIME],
            'region': 'ES',
            'minAge': 6,
            'maxAge': 18
        }
    }

    return data


def test_post_movies(filter_data):
    response = client.post('/movies', json=filter_data)
    json_response = response.json()

    assert response.status_code == 200
    assert 'filteredMovies' in json_response.keys()
    assert 'maxPages' in json_response.keys()

    assert len(json_response['filteredMovies']) > 0
    assert json_response['maxPages'] > 0


def test_post_movies_pagination(filter_data):
    filter_data['page'] = 2

    response = client.post('/movies', json=filter_data)
    json_response = response.json()

    assert response.status_code == 200
    assert 'filteredMovies' in json_response.keys()
    assert 'maxPages' in json_response.keys()

    assert len(json_response['filteredMovies']) > 0


def test_post_recommendations(filter_data):
    data = {
        **filter_data,
        'selectedMovies': [
            {
                "movieId": 2959,
                "valoration": 1
            },
            {
                "movieId": 2985,
                "valoration": -1
            },
            {
                "movieId": 6874,
                "valoration": 1
            }
        ]
    }

    response = client.post('/recommendations', json=data)
    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response) > 0
