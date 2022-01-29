from pydantic import BaseConfig

class AppConfig(BaseConfig):
    NUM_MOVIES: int = 20
    NUM_RECOMMENDATIONS: int = 50
    TMDB_API_URL: str = 'https://api.themoviedb.org/3'
    TMDB_PAGE_URL: str = 'https://www.themoviedb.org/movie/'
    TMDB_POSTER_URL: str = 'https://image.tmdb.org/t/p/original'
    YOUTUBE_URL: str = 'https://youtube.com/watch?v='


app_config = AppConfig()
