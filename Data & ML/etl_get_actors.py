#!/usr/bin/env python

# For all the movies in movies.csv that have a value of tmdbId, call the The 
# Movie Database API to obtain the actors (cast).
# The results are stored in movie_actors.csv

# See doc of the moviedb API:
# https://developers.themoviedb.org/3/getting-started/introduction 
# 
# **Important**: The configuration file "tmdb_api_key" must be in the same
# folder as this program. It contains a valid key for themoviedb API (one line)

max_actors_per_movie = 10

# Set environment to 'test' or 'prod'
environment='prod'

import pandas as pd
import json

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

# The ETL will write the results in the input_directory
# (input_directory will be the input for the model, but the output of the ETL)
dir_etl_out = config['dir_data_input']

# Import movies dataset
df_movies = pd.read_csv(dir_etl_out + '/movies.csv')
df_movies.head()

import requests
import pandas as pd

# First part of the URL for API call
url = "https://api.themoviedb.org/3/movie/"
# Example of full URL to obtain data for movie 11862: 
# "https://api.themoviedb.org/3/movie/11862/credits"

# The file tmdb_api_key must contain a valid key to access the API.
with open('tmdb_api_key', 'r') as f:
    api_key =  f.read()
f.closed
parameters = {"api_key":api_key}

'''
As an example of the structure that the API returns, this is a possible value
of result['cast']:
[{'adult': False,
   'gender': 2,
   'id': 67773,
   'known_for_department': 'Acting',
   'name': 'Steve Martin',
   'original_name': 'Steve Martin',
   'popularity': 9.386,
   'profile_path': '/d0KthX8hVWU9BxTCG1QUO8FURRm.jpg',
   'cast_id': 1,
   'character': 'George Banks',
   'credit_id': '52fe44959251416c75039eb9',
   'order': 0},
'''

print("Progress ('.' = 100 movies, 'k' = 1k movies, '|' = 10k movies):")
# For each movie with 100+ ratings that exists in tmdbId, 
# call API to obtain actors data
movie_actors = []
for index, movie_row in df_movies.iterrows():
    if movie_row['num_ratings']>=100 and movie_row['tmdbId'] > 0:
        movieId = movie_row['movieId']
        tmdbId = int(movie_row['tmdbId'])
        # Get data from API for the current movie
        response = requests.get(url + str(tmdbId) +
            '/credits', params=parameters)
        result = response.json()
        if len(result)>0 and 'cast' in result:
            # There is cast data for this movie
            # For each actor, get data into movie_actors
            for actor in result['cast']:
                # Do not store more actors than the required maximum
                if actor['order'] < max_actors_per_movie:
                    movie_actors.append({'movieId':movieId, 'tmdbId':tmdbId,
                        'actor_tmdb_id':actor['id'], 'actor_name':actor['name'],\
                        'role':actor['character'], 'profile_path':actor['profile_path']})

    if index>=10000 and index%10000 == 0:
        print('|', end='', flush=True)  # Write '|' every 10k movies
    elif index>=1000 and index%1000 == 0:
        print('k', end='', flush=True)  # Write 'k' every 1k movies
    elif index>=100 and index%100 == 0:
        print('.', end='', flush=True)  # Write '.' every 100 movies
        
df_movie_actors = pd.DataFrame(movie_actors)

# Export to csv
df_movie_actors.to_csv(dir_etl_out +
    '/movie_actors.csv', index=False)
print('\nmovie_actors dataset created', df_movie_actors.shape)
