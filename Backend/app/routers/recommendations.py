import os
import asyncio
import aiohttp
from fastapi import APIRouter
from typing import List

from app.models.types import Genre, Platform
from app.models.movies import MovieRecommendation
from app.models.users import UserSelectionFilter
from app.db import aggregates
from app.recommenders.make_predictions import predictor
from app.routers.utils import async_request
from app.config import app_config

router = APIRouter(
    tags=['recommendations']
)

async def get_movies_extra_details(tmdb_ids: List[int]):
    params = {'api_key': os.environ.get('TMDB_API_KEY')}
    num_movies = len(tmdb_ids)

    async with aiohttp.ClientSession() as session:
        tmdb_api_movie_url = f'{app_config.TMDB_API_URL}/movie'

        details_tasks = [
            async_request(session, f'{tmdb_api_movie_url}/{tmdb_id}', params)
            for tmdb_id
            in tmdb_ids
        ]

        trailer_tasks = [
            async_request(session, f'{tmdb_api_movie_url}/{tmdb_id}/videos', params)
            for tmdb_id
            in tmdb_ids
        ]

        results = await asyncio.gather(*details_tasks, *trailer_tasks)

        # The details are the first half of the list, whereas the trailers can
        # be found in the other half
        details_results = results[:num_movies]
        trailers_results = results[num_movies:]

        extra_information = list(
            map(
                lambda details_trailers: {
                    'thumbnail': f"{app_config.TMDB_POSTER_URL}{details_trailers[0]['poster_path']}",
                    'description': details_trailers[0]['overview'],
                    'averageUserScore': details_trailers[0]['vote_average'],
                    'trailer': f"{app_config.YOUTUBE_URL}{details_trailers[1]['results'][0]['key']}"
                        if len(details_trailers[1]['results'])
                        else ''
                },
                zip(details_results, trailers_results)
            )
        )

        return extra_information


@router.post('/recommendations', response_model=List[MovieRecommendation])
async def create_movie_recommendations(user_selection: UserSelectionFilter):
    matching_movies = aggregates.find_matching_movies(user_selection.filter)
    user_selected_movies = aggregates.find_user_selected_movies(user_selection.selectedMovies)

    # Get the first 50 recommendations
    recommendations = predictor(user_selected_movies, matching_movies)
    recommendations = recommendations[:app_config.NUM_RECOMMENDATIONS]

    recommendations_details = aggregates.get_recommended_movies_details(
        recommendations,
        user_selection.filter.region
    )

    # Get extra information
    tmdb_ids = list(map(lambda movie: movie['tmdbId'], recommendations_details))
    extra_information = await get_movies_extra_details(tmdb_ids)

    # Merge movies details with extra information
    recommendations_details = [
        {**details, **extra}
        for details, extra 
        in zip(recommendations_details, extra_information)
    ]

    # Filter out unsupported platforms and genres and remove unused field
    for movie in recommendations_details:
        movie['platforms'] = list(
            filter(
                lambda platform: platform in Platform,
                movie['platforms']
            )
        )

        movie['genres'] = list(
            filter(
                lambda genre: genre in Genre,
                movie['genres']
            )
        )

        movie['tmdbUrl'] = f"{app_config.TMDB_PAGE_URL}{movie['tmdbId']}/watch?locale={user_selection.filter.region}"

        del movie['tmdbId']

    return recommendations_details
