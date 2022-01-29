from iso3166 import countries

from typing import List, Optional
from pydantic import BaseModel, validator

from .types import Genre, Platform

class MoviesFilter(BaseModel):
    genres: List[Genre]
    minLength: int
    maxLength: int
    platforms: List[Platform]
    region: str
    minAge: int
    maxAge: int

    @validator('minLength')
    def validate_min_length(cls, min_length):
        if min_length < 0:
            raise ValueError('minLength must be greater or equal than 0')

        return min_length


    @validator('maxLength')
    def validate_max_length(cls, max_length, values):
        if max_length < 0 or max_length < values['minLength']:
            raise ValueError('maxLength must be greater or equal than 0 and greater or equal than minLength')

        return max_length


    @validator('region')
    def validate_region(cls, region):
        try:
            countries.get(region)
        except KeyError:
            raise ValueError('Invalid region code')

        return region


    @validator('minAge')
    def validate_min_age(cls, min_age):
        if min_age < 0:
            raise ValueError('minAge must be greater or equal than 0')

        return min_age


    @validator('maxAge')
    def validate_max_age(cls, max_age, values):
        if max_age < 0 or max_age < values['minAge']:
            raise ValueError('maxAge must be greater or equal than 0 and greater or equal than minAge')

        return max_age


class UserMoviesFilter(BaseModel):
    filter: MoviesFilter
    page: Optional[int] = 1

    @validator('page')
    def validate_page(cls, page):
        if page < 1:
            raise ValueError('page must be greater or equal than 1')

        return page


class SelectedMovie(BaseModel):
    movieId: int
    valoration: int

    @validator('valoration')
    def validate_valoration(cls, valoration):
        if valoration != -1 and valoration != 1:
            raise ValueError('valoration must be either -1 for disliked movies or 1 for liked movies')

        return valoration


class UserSelectionFilter(BaseModel):
    selectedMovies: List[SelectedMovie]
    filter: MoviesFilter
