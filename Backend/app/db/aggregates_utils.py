from app.models.users import MoviesFilter
from app.db.db_session import database_instance

recommender_projection_stage = {
    '$project': {
        '_id': 0,
        'movieId': 1,
        'year': 1,
        'num_ratings': 1,
        'avg_rating': 1,
        'isAdult': 1,
        'runtimeMinutes': 1,
        'director': 1,
        'genres': {
            '$map': {
                'input': '$genres',
                'as': 'genre',
                'in': {
                    '$toLower': '$$genre'
                }
            }
        }
    }
}

def create_filter_match_stage(filter: MoviesFilter):
    filter_match_stage = {
        '$match': {
            'runtimeMinutes': {
                '$gte': filter.minLength,
                '$lte': filter.maxLength
            },
            'genres': {
                '$in': filter.genres
            },
            f'platforms.{filter.region}': {
                '$in': filter.platforms,
            },
            'age_restriction': {
                '$gte': filter.minAge,
                '$lte': filter.maxAge
            }
        }
    }

    return filter_match_stage


def run_aggregate(*pipeline):
    cursor = database_instance.movies_collection.aggregate(list(pipeline))

    return list(cursor)
