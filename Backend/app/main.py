from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import movies, recommendations
from app.db.db_session import database_instance
from app.recommenders.Recommender import recommender

app = FastAPI(
    title='Get Me A Movie API'
)

# Declare CORS policy
origins = ['*']

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def start_mongo_connection():
    database_instance.create_connection()


@app.on_event('shutdown')
def close_mongo_connection():
    database_instance.close_connection()


# Include different routers into the app
app.include_router(movies.router)
app.include_router(recommendations.router)

@app.get('/')
def get_root():
    return {'status': 'OK'}
