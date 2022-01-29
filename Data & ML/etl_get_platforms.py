#!/usr/bin/env python

# For all the movies in movies.csv that have a value of tmdbId, call the The 
# Movie Database API to obtain information on the platforms where the movie is
# available.
# There are different values for each region.
# The results are stored in movie_region_platforms.csv

# See doc of the moviedb API:
# https://developers.themoviedb.org/3/getting-started/introduction 
# 
# **Important**: The configuration file "tmdb_api_key" must be in the same
# folder as this program. It contains a valid key for themoviedb API (one line)

# Set environment to 'test' or 'prod'
environment='test'

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
# "https://api.themoviedb.org/3/movie/11862/watch/providers"

# The file tmdb_api_key must contain a valid key to access the API.
with open('tmdb_api_key', 'r') as f:
    api_key =  f.read()
f.closed
parameters = {"api_key":api_key}

'''
As an example of the structure that the API returns, this is a possible value
of result['results']['ES']['flatrate']:

[{'display_priority': 8,
  'logo_path': '/j3SNvXPH2hRvH7MEvc2fGRLt9q2.jpg',
  'provider_id': 63,
  'provider_name': 'Filmin'},
 {'display_priority': 10,
  'logo_path': '/3kZQY7nIwC5sIJmURyF6W91pAkg.jpg',
  'provider_id': 149,
  'provider_name': 'Movistar Plus'}]
'''

print("Progress ('.' = 100 movies, 'k' = 1k movies, '|' = 10k movies):")
# For each movie with 100+ ratings that exists in tmdbId, 
# call API to obtain (country,certification)
movie_region_platforms = []
for index, movie_row in df_movies.iterrows():
    if movie_row['num_ratings']>=100 and movie_row['tmdbId'] > 0:
        # Get data from API for the current movie
        response = requests.get(url + str(movie_row['tmdbId']) +
            '/watch/providers', params=parameters)
        result = response.json()
        if 'results' in result:  # If no data found, this key is not present
            # For each region, get platforms into movie_region_platforms
            for region in result['results']:
                # Platforms: string with each platform separated by '|'
                platforms=''
                if 'flatrate' in result['results'][region]:
                    for provider in result['results'][region]['flatrate']:
                        platforms = platforms + provider['provider_name'] + '|'
                # movie_region_platforms has one record per movie+region, 
                # and only if there is at least one platform informed.
                if platforms != '':
                    platforms = platforms[:-1]  # Remove last separator
                    movie_region_platforms.append({'movieId':movie_row['movieId'],
                        'region':region, 'platforms':platforms})

    if index>=10000 and index%10000 == 0:
        print('|', end='', flush=True)  # Write '|' every 10k movies
    elif index>=1000 and index%1000 == 0:
        print('k', end='', flush=True)  # Write 'k' every 1k movies
    elif index>=100 and index%100 == 0:
        print('.', end='', flush=True)  # Write '.' every 100 movies

df_movie_region_platforms = pd.DataFrame(movie_region_platforms)

# Export to csv
df_movie_region_platforms.to_csv(dir_etl_out + '/movie_region_platforms.csv',
    index=False)
print('movie_region_platforms dataset created', df_movie_region_platforms.shape)
