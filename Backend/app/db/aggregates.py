from typing import List
import pymongo

from app.models.users import MoviesFilter, SelectedMovie, UserMoviesFilter
from app.db.db_session import database_instance
from app.db import aggregates_utils
from app.config import app_config

def aggregate_filter_movies(user_movies_filter: UserMoviesFilter):
    num_movies_skip = app_config.NUM_MOVIES * (user_movies_filter.page - 1)

    stage_match_options = aggregates_utils.create_filter_match_stage(user_movies_filter.filter)

    # The facet stage is applied on the result of the previous match and generates
    # a list containing the filtered movies and the number of movies found in that
    # match, which will be later transformed in the maximum number of pages that
    # can be queried
    stage_facet = {
        '$facet': {
            'filteredMovies': [
                {
                    '$sort': {
                        'num_ratings': pymongo.DESCENDING,
                        'avg_rating': pymongo.DESCENDING,
                        '_id': pymongo.DESCENDING
                    }
                },
                {
                    '$skip': num_movies_skip
                },
                {
                    '$limit': app_config.NUM_MOVIES
                },
                {
                    '$project': {
                        '_id': 0,
                        'movieId': 1,
                        'title': 1,
                        'year': 1,
                        'tmdbId': 1
                    }
                }
            ],
            'maxPages': [
                {
                    '$count': 'count'
                },
            ]
        }
    }

    # Extract object from array
    stage_unwind = {
        '$unwind': '$maxPages'
    }

    # Replace value of maxPages so that is a number instead of an object
    stage_replace_value = {
        '$set': {
            'maxPages': {
                '$toInt': {
                    '$ceil': {
                        '$divide': ['$maxPages.count', app_config.NUM_MOVIES]
                    }
                }
            }
        }
    }

    result = aggregates_utils.run_aggregate(
        stage_match_options,
        stage_facet,
        stage_unwind,
        stage_replace_value
    )

    matching_movies = (
        result[0] if result
        else {'filteredMovies': [], 'maxPages': 0}
    )

    return matching_movies


def find_matching_movies(filter: MoviesFilter):
    stage_match_options = aggregates_utils.create_filter_match_stage(filter)

    matching_movies = aggregates_utils.run_aggregate(
        stage_match_options,
        aggregates_utils.recommender_projection_stage
    )

    return matching_movies


def find_user_selected_movies(selected_movies: List[SelectedMovie]):
    movies_valorations = {
        movie.movieId: movie.valoration
        for movie in selected_movies
    }

    stage_match_options = {
        '$match': {
            'movieId': {
                '$in': list(movies_valorations.keys())
            }
        }
    }

    matching_movies = aggregates_utils.run_aggregate(
        stage_match_options,
        aggregates_utils.recommender_projection_stage
    )

    for movie in matching_movies:
        movie['valoration'] = movies_valorations[movie['movieId']]

    return matching_movies


def get_recommended_movies_details(recommended_ids: List[int], region: str):
    stage_match_options = {
        '$match': {
            'movieId': {
                '$in': recommended_ids
            }
        }
    }

    stage_project = {
        '$project': {
            '_id': 0,
            'movieId': 1,
            'tmdbId': 1,
            'title': 1,
            'year': 1,
            'ageRestriction': '$age_restriction',
            'duration': '$runtimeMinutes',
            'genres': 1,
            'platforms': f'$platforms.{region}',
            'director': 1,
            'cast': {
                '$map': {
                    'input': '$cast',
                    'as': 'actor',
                    'in': {
                        'name': '$$actor.name',
                        'role': '$$actor.role',
                        'image': '$$actor.profile_path'
                    }
                }
            }
        }
    }

    matching_movies = aggregates_utils.run_aggregate(
        stage_match_options,
        stage_project
    )

    # Generate link to actors photos only if the path field is valid
    for movie in matching_movies:
        for actor in movie['cast']:
            actor['image'] = (
                '' if isinstance(actor['image'], float)
                else f"{app_config.TMDB_POSTER_URL}{actor['image']}"
            )

    # Since Mongo messes up with the order of the recommended movies, it has to
    # be restored
    matching_movies = [
        matching_movies[idx]
        for id in recommended_ids
        for idx, movie in enumerate(matching_movies)
        if movie['movieId'] == id
    ]

    return matching_movies
