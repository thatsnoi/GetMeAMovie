#!/usr/bin/env python

# For all the movies in movies.csv that have a value of tmdbId, call the The 
# Movie Database API to obtain information on the age restriction
# ("certification").
# There are different values for each country.
# The results are stored in movie_country_certification.csv

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
# (input_directory will be the input for the model, but it is the output of the ETL)
dir_etl_out = config['dir_data_input']

# Import movies dataset
df_movies = pd.read_csv(dir_etl_out + '/movies.csv')
df_movies.head()

import requests
import pandas as pd

# First part of the URL for API call
url = "https://api.themoviedb.org/3/movie/"
# Example of full URL to obtain data for movie 11862: 
# "https://api.themoviedb.org/3/movie/11862/release_dates"

# The file tmdb_api_key must contain a valid key to access the API.
with open('tmdb_api_key', 'r') as f:
    api_key =  f.read()
f.closed
parameters = {"api_key":api_key}

'''
As an example of the structure that the API returns, this is a possible value
of "result". The field of interest for us is "certification".

{'id': 238,
 'results': [{'iso_3166_1': 'HK',
   'release_dates': [{'certification': '',
     'iso_639_1': '',
     'note': '',
     'release_date': '1980-01-24T00:00:00.000Z',
     'type': 3}]},
  {'iso_3166_1': 'KR',
   'release_dates': [{'certification': '18',
     'iso_639_1': '',
     'note': '',
     'release_date': '1972-12-27T00:00:00.000Z',
     'type': 3}]},
'''

print("Progress ('.' = 100 movies, 'k' = 1k movies, '|' = 10k movies):")
# For each movie with 100+ ratings that exists in tmdbId, 
# call API to obtain (country,certification)
movie_country_certification = []
for index, movie_row in df_movies.iterrows():
    if movie_row['num_ratings']>=100 and movie_row['tmdbId'] > 0:
        # Get data from API for the current movie
        response = requests.get(url + str(movie_row['tmdbId']) +
            '/release_dates', params=parameters)
        result = response.json()
        if 'results' in result:  # If no data found, this key is not present
            # For each country, get certification into movie_country_certification
            for country_data in result['results']:
                if 'release_dates' in country_data:
                    certification = country_data['release_dates'][-1]['certification']
                # movie_country_certification has one record per movie+country,
                # and only if certification is informed.
                if certification != '':
                    movie_country_certification.append(
                        {'movieId':movie_row['movieId'], 'country':country_data['iso_3166_1'],
                         'certification':certification})

    if index>=10000 and index%10000 == 0:
        print('|', end='', flush=True)  # Write | every 10k movies
    elif index>=1000 and index%1000 == 0:
        print('k', end='', flush=True)  # Write k every 1k movies
    elif index>=100 and index%100 == 0:
        print('.', end='', flush=True)  # Write . every 100 movies

df_movie_country_certification = pd.DataFrame(movie_country_certification)

# Export to csv
df_movie_country_certification.to_csv(dir_etl_out +
    '/movie_country_certification.csv', index=False)
print('movie_country_certification dataset created', df_movie_country_certification.shape)
