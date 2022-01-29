import os
import asyncio
import aiohttp
from fastapi import APIRouter
from typing import List

from app.models.movies import MovieSelection
from app.models.users import UserMoviesFilter
from app.db.aggregates import aggregate_filter_movies
from app.routers.utils import async_request
from app.config import app_config

router = APIRouter(
    tags=['movies']
)

async def get_movies_thumbnails(tmdb_ids: List[int]):
    params = {'api_key': os.environ.get('TMDB_API_KEY')}

    async with aiohttp.ClientSession() as session:
        tasks = [
            async_request(session, f'{app_config.TMDB_API_URL}/movie/{tmdb_id}', params)
            for tmdb_id
            in tmdb_ids
        ]

        results = await asyncio.gather(*tasks)

        # Process results getting the thumbnails and the indexes of the movies
        # for which no information could be found
        thumbnails = [
            f"{app_config.TMDB_POSTER_URL}{movie['poster_path']}"
            for movie in results
            if movie is not None
        ]

        remove_idx = [idx for idx, movie in enumerate(results) if movie is None]

        return thumbnails, reversed(remove_idx)


@router.post('/movies', response_model=MovieSelection)
async def create_movies_list(user_movies_filter: UserMoviesFilter):
    matching_movies = aggregate_filter_movies(user_movies_filter)

    tmdb_ids = list(
        map(
            lambda movie: movie['tmdbId'],
            matching_movies['filteredMovies']
        )
    )

    thumbnails, remove_idx = await get_movies_thumbnails(tmdb_ids)

    for idx in remove_idx:
        del matching_movies['filteredMovies'][idx]

    for movie, thumbnail in zip(matching_movies['filteredMovies'], thumbnails):
        movie['thumbnail'] = thumbnail
        del movie['tmdbId']

    return matching_movies
