#!/usr/bin/env python

# Two configuration files are required, in the same directory as this notebook:
# - config_test.json or config_prod.json (depending on environment)  
# Configures the input and output directories and the database parameters (except the password).
# - db_credentials.txt  
# Contains the password of the database user. **Do not upload this file to git**.
# 
# This program uploads the movies dataset including the fields required for filtering, which are:
# genres, age restriction, runtimeMinutes, platform, num_ratings, avg_rating, year

import pandas as pd
import json
import math

# Set environment to 'test' or 'prod'
environment='test'

# Read configuration file
if environment=='test':
    with open('config_test.json', 'r') as fp:
        config = json.load(fp)
elif environment=='prod':
    with open('config_prod.json', 'r') as fp:
        config = json.load(fp)
else:
    print("Error: environment must be 'test' or 'prod'")

print('Environment:', environment)
print(config)

# Connect to MongoDB
db_url = config['db_url']
db_name = config['db_name']
db_user = config['db_user']

import pymongo
import ssl
try:
    # Read from db_credentials.txt password required to connect to MongoDB.
    with open("db_credentials.txt", 'r') as f:
        [db_password] = f.read().splitlines()
    
    # Connect
    conn=pymongo.MongoClient("mongodb+srv://{}:{}@{}" \
        .format(db_user, db_password, db_url), ssl_cert_reqs=ssl.CERT_NONE)
    print ("Connected successfully to MongoDB")
    
except pymongo.errors.ConnectionFailure as e:
    print ("Could not connect to MongoDB: %s" % e) 

# Open database
db = conn[db_name]

########################################
# Extract                              #
########################################

data_directory = config['dir_data_input']

df_platforms   = pd.read_csv(data_directory + '/movie_region_platforms.csv')
print('Read Platforms dataset:', df_platforms.shape)

df_certification   = pd.read_csv(data_directory + '/movie_country_certification.csv')
print('Read Certifications dataset:', df_certification.shape)

df_directors = pd.read_csv(data_directory + '/directors.csv',
    usecols=['directorId', 'name']).rename(columns={'name':'director'})
print('Read Directors dataset:', df_directors.shape)

df_cast = pd.read_csv(data_directory + '/movie_actors.csv')
print('Read movie_actors dataset:', df_cast.shape)

df_movies = pd.read_csv(data_directory + '/movies.csv',
    usecols=['movieId', 'imdbId', 'tmdbId', 'title', 'year', 'num_ratings',
             'avg_rating', 'isAdult','runtimeMinutes', 'genres', 'directorId'])
print('Read Movies dataset:', df_movies.shape)

# Only movies with at least 100 ratings will go in the DB
df_movies = df_movies[df_movies.num_ratings >= 100]

# Get list of movie ids that exist in the model
col_similarity = db['similarity_CF']
df_movies_in_model = pd.DataFrame(list(col_similarity.find( {}, {'movieId':1, '_id':0} )))

if len(df_movies_in_model)<=0:
    raise ValueError('Table similarity_CF was not found in the database or is empty')

# Keep only movies that exist in the model
df_movies = pd.merge(df_movies, df_movies_in_model)
print('Movies to be uploaded to DB:', str(len(df_movies)))

# Add director name to df_movies
df_movies = pd.merge(df_movies, df_directors, how='left').drop(columns='directorId')

########################################
# Transform                            #
########################################

# Arrange movie-region-platform data as required in the database
# Example:
# {'movieId': 1,
#   'platforms': {
#    'DE': ['DISNEY', 'NETFLIX'],
#    'ES': ['DISNEY']}
d_platforms = []
for group_name, df_group in df_platforms.groupby('movieId'):
    platforms = {}
    for row_index, row in df_group.iterrows():
        platforms_abr = row.platforms.upper().replace('AMAZON PRIME VIDEO', 'PRIME')
        platforms_abr = platforms_abr.replace('DISNEY PLUS', 'DISNEY')
        platforms[row.region] = platforms_abr.split('|')
    d_platforms.append({'movieId':group_name, 'platforms':platforms})

# Create a dictionary that provides, for each movieId, the list of actors (cast)
# in the format required in the DB. Example of one actor:
# {'tmdb_name_id':738, 'name':'Sean Connery', 'role':'Professor Henry Jones',
#  'profile_path': '/jYCw9CzHbBkdVpTXGtnmbaCStoL.jpg'}
max_actors_per_movie = 5
d_cast = {}
for movieId, df_group in df_cast.groupby('movieId'):
    actors = []
    for row_index, actor in df_group.iterrows():
        if len(actors) < max_actors_per_movie:
            actors.append({'tmdb_name_id':actor.actor_tmdb_id, 'name':actor.actor_name,
                           'role':actor.role, 'profile_path':actor.profile_path})
    d_cast[movieId] = actors

# Use age certifications from Germany
df_certification = df_certification[df_certification.country=='DE']
# Ensure there are no movieId duplicates
df_certification.drop_duplicates('movieId', keep='first')
# Convert into int (default 18 if not a number)
df_certification['certification'] = df_certification['certification'].\
    apply(lambda x: int(x) if x.isdigit() else 18)
# Dictionary to look up certification value of a movie
d_certification = dict(zip(df_certification.movieId, df_certification.certification))

dict_movies = df_movies.to_dict(orient='records')
# Obtain "platform" and "age_restriction". Transform some variables.
for movie in dict_movies:
    movieId = movie['movieId']

    # Platforms - look up d_platforms
    for movie_platforms in d_platforms:
        if movie_platforms['movieId'] == movieId:
            movie['platforms'] = movie_platforms['platforms']

    # age_restriction - look up d_certification
    movie['age_restriction'] = d_certification.get(movieId, 18)
    
    # genres: convert to list
    movie['genres'] = movie['genres'].split('|')

    # Cast: look up d_cast
    if movieId in d_cast:
        movie['cast'] = d_cast[movieId]
    else:
        movie['cast'] = []

    # Avoid the ".0" in integer variables tmdbId, year, isAdult, runtimeMinutes,
    # num_ratings
    if  pd.notna(movie['tmdbId']):
        movie['tmdbId'] = math.trunc(movie['tmdbId'])
    if  pd.notna(movie['year']):
        movie['year'] = math.trunc(movie['year'])
    if  pd.notna(movie['isAdult']):
        movie['isAdult'] = math.trunc(movie['isAdult'])
    if  pd.notna(movie['runtimeMinutes']):
        movie['runtimeMinutes'] = math.trunc(movie['runtimeMinutes'])
    if  pd.notna(movie['num_ratings']):
        movie['num_ratings'] = math.trunc(movie['num_ratings'])

########################################
# Load                                 #
########################################

col_movies = db['movies']

# Delete previous data in the collection
col_movies.delete_many({})

# Store movies dataset
col_movies.insert_many(dict_movies)
print('Uploaded dataset Movies. #records:', col_movies.count_documents({}))

# Close connection to MongoDB
conn.close()
