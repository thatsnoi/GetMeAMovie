from pydantic import BaseModel

from typing import List, Optional

from .types import Genre, Platform

class Cast(BaseModel):
    name: str
    role: str
    image: str

class BaseMovie(BaseModel):
    movieId: int
    title: str
    year: int
    thumbnail: Optional[str]

class MovieSelection(BaseModel):
    filteredMovies: List[BaseMovie]
    maxPages: int

class MovieRecommendation(BaseMovie):
    description: str
    genres: List[Genre]
    duration: int
    ageRestriction: int
    averageUserScore: float
    director: str
    cast: List[Cast]
    platforms: List[Platform]
    trailer: str
    tmdbUrl: str
