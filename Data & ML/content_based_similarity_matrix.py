import warnings
import numpy as np
import time
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
warnings.filterwarnings('ignore')
pd.options.display.max_columns = 500


# Read meta data about movies
md = pd.read_csv('../data/input/movies_metadata.csv')
movies = pd.read_csv('../data/input/movies.csv')
directors = pd.read_csv('../data/input/directors.csv')
ids_to_use = np.loadtxt('movieIds_TO_USE.txt')


# Need to drop these wrong entries
md = md.drop([19730, 29503, 35587])

# Take meta data about movies with mapping
md['id'] = md['id'].astype('int')

# Add directors and movielens id
movies = movies.merge(directors[['directorId', 'name']], on = 'directorId')
movies = movies.rename({'name':'director_name', 'imdbId':'imdb_id'}, axis=1)
smd = md.merge(movies[['director_name', 'imdb_id', 'movieId']], on='imdb_id')

# FILTER BY MOVIES WITH AT LEAST 100 REVIEWS
smd = smd[smd['movieId'].isin(ids_to_use)]

# Preprocess tagline and description

smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline'] + smd['director_name']
smd['description'] = smd['description'].fillna('')

# Drop duplicates

smd = smd.loc[smd['movieId'].drop_duplicates().index]

# Apply and create TF-IDF features

start_time = time.time()
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print(f'Time to train was: {time.time() - start_time} seconds')

print(f'Similarity matrix shape is : {cosine_sim.shape} rows x columns')

# Saving with 4 decimals, change it if needed
np.savetxt('content_based_matrix.txt', cosine_sim, fmt='%1.4f')
# Saving index
pd.DataFrame({"index": smd.index, "movieId": smd['movieId'], "title":smd['title']}).to_csv('index.txt', index=False)