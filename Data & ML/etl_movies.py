# ETL of movie data
# Transform and integrate data from the movielens and imdb databases
# Source: csv datasets in data/raw
# Target: csv datasets in data/input (which is the input of the model)
# In test environment, the source and target are data/raw/test, data/input/test

# Set environment to 'test' or 'prod'
environment='test'

import numpy as np
import pandas as pd
import json

# Read configuration file - contains directories and database connection details
if environment=='test':
    with open('config_test.json', 'r') as fp:
        config = json.load(fp)
elif environment=='prod':
    with open('config_prod.json', 'r') as fp:
        config = json.load(fp)
else:
    raise ValueError('environment must be "test" or "prod"')

print('Running on environment:', environment)
print(config)

# The ETL will read from raw_directory and write the results in the input_directory
# (input_directory will be the input for the model, but it is the output of the ETL)
dir_etl_in = config['dir_data_raw']
dir_etl_out = config['dir_data_input']

#########################################################
# Import and process movielens data
#########################################################

# Import data
df_movies  = pd.read_csv(dir_etl_in + '/movies.csv')
print('movielens movies dataset imported', df_movies.shape)

df_ratings = pd.read_csv(dir_etl_in + '/ratings.csv')
print('movielens ratings dataset imported', df_ratings.shape)

df_tags    = pd.read_csv(dir_etl_in + '/tags.csv')
print('movielens tags dataset imported', df_tags.shape)

df_links   = pd.read_csv(dir_etl_in + '/links.csv')
print('movielens links dataset imported', df_links.shape)

# Transform df_movies

# Get column with imdbId from df_links
# First adapt to the format in the imdb dataset by converting to char with the 'tt' prefix
df_links['imdbId'] = 'tt' + df_links['imdbId'].apply(lambda x: str(x).zfill(7))
df_movies = pd.merge(df_movies, df_links, how='left')

# Split title and year (In movielens the title has the year in parentheses at the end)
pattern = "(?P<title>.*) \((?P<year>\d{4})\)"
title_year = df_movies.title.str.extract(pattern, expand= True)
df_movies['title'] = title_year['title']
df_movies['year'] = title_year['year']

# Add number of ratings and average rating
df_ratings_agg = df_ratings[['movieId', 'rating']].groupby(['movieId']) \
    .agg({'movieId':'size', 'rating':'mean'}) \
    .rename(columns={'movieId':'num_ratings','rating':'avg_rating'}).reset_index()
df_ratings_agg.avg_rating = round(df_ratings_agg.avg_rating, 2)
df_movies = pd.merge(df_movies, df_ratings_agg)

# Convert genres into 0-1 dummy variables
df_movies['genres'] = df_movies['genres'].str.lower()
df_movies = pd.concat([df_movies, df_movies['genres'].str.get_dummies(sep='|')], axis=1)
df_movies.rename(columns={"(no genres listed)": "no_genres"}, inplace=True)
# On the other hand, in the "genres" list the values are uppercase, as prefered by the backend.
df_movies['genres'] = df_movies['genres'].str.upper()

# Transform df_ratings

# Obtain date from timestamp
df_ratings['rating_date'] = pd.to_datetime(df_ratings['timestamp'], unit='s').dt.date
df_ratings.drop(columns='timestamp', inplace=True)

# Transform df_tags

# Obtain date from timestamp
df_tags['tag_date'] = pd.to_datetime(df_tags['timestamp'], unit='s').dt.date
df_tags.drop(columns='timestamp', inplace=True)

#########################################################
# Import and process imdb data
#########################################################

df_imdb_titles  = pd.read_csv(dir_etl_in + '/imdb_title.tsv', sep='\t', na_values='\\N').drop(
    columns=['endYear', 'primaryTitle', 'originalTitle', 'startYear', 'genres'])
print('imdb_title dataset imported', df_imdb_titles.shape)

df_crew  = pd.read_csv(dir_etl_in + '/imdb_crew.tsv', sep='\t', na_values='\\N') \
    .drop(columns='writers')
print('imdb_crew dataset imported', df_crew.shape)

# df_principals  = pd.read_csv(dir_etl_in + '/imdb_principals.tsv', sep='\t', na_values='\\N')
# print('imdb_principals dataset imported', df_principals.shape)

df_names  = pd.read_csv(dir_etl_in + '/imdb_name.tsv', sep='\t', na_values='\\N').drop(
    columns=['primaryProfession', 'knownForTitles'])
print('imdb_name dataset imported', df_names.shape)

# From the titles dataset, we only want movies (total of 593,400 movies)
df_imdb_titles = df_imdb_titles[df_imdb_titles.titleType=='movie']
df_imdb_titles.drop(columns='titleType', inplace=True)

# Process imdb data
# Merge directors into titles
df_imdb_titles = pd.merge(df_imdb_titles, df_crew, how='left')

# Rename id
df_imdb_titles.rename(columns={"tconst": "imdbId"}, inplace=True)

# Store the first director in new column "director"
df_imdb_titles['directorId'] = (df_imdb_titles.directors.str.split(",")).str[0]

# Add imdb data to df_movies
df_movies = pd.merge(df_movies, df_imdb_titles, how='left')

# Rearrange column order in df_movies
df_movies = df_movies.reindex(['movieId', 'imdbId', 'tmdbId', 'title', 'year',
    'num_ratings', 'avg_rating', 'isAdult', 'runtimeMinutes',
    'directors', 'directorId', 'no_genres','action', 'adventure', 'animation',
    'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy',
    'film-noir', 'horror', 'imax', 'musical', 'mystery', 'romance', 'sci-fi',
    'thriller', 'war', 'western', 'genres'], axis=1)

# Create table with director details
df_directors = df_names[df_names.nconst.isin(df_movies['directorId'])].rename(
    columns={'nconst': 'directorId', 'primaryName':'name'})

# Export to csv
df_movies.to_csv(dir_etl_out + '/movies.csv', index=False)
print('movies dataset created', df_movies.shape)

df_ratings.to_csv(dir_etl_out + '/ratings.csv', index=False)
print('ratings dataset created', df_ratings.shape)

df_tags.to_csv(dir_etl_out + '/tags.csv', index=False)
print('tags dataset created', df_tags.shape)

df_directors.to_csv(dir_etl_out + '/directors.csv', index=False)
print('directors dataset created', df_directors.shape)
