import pandas as pd
import numpy as np
import json
import itertools as it
import pymongo
import ssl
from tqdm import tqdm
import sys
import warnings
warnings.filterwarnings('ignore')


# Load data ---------------
all_ratings = pd.read_csv('/Users/irenebonafonte/Documents/MasterDS/AgileDS/GMAM_noGit/data_for_model/ratings_split'+str(sys.argv[1])+'.csv')
# all_ratings = pd.read_csv('/Users/irenebonafonte/Documents/MasterDS/AgileDS/GMAM_noGit/data_for_model/ratings_split'+str(i)+'.csv')
all_ratings[['CF_prediction','CB_prediction']] = np.nan
all_ratings = all_ratings.sort_values('movieId')
all_ratings.loc[all_ratings.binary_rating == 0,'binary_rating'] = -1

# Load similarity matrices -----------
# Connect to database
with open('config_prod.json', 'r') as fp:
    config = json.load(fp)
    
# Connect to MongoDB
db_url = config['db_url']
db_name = config['db_name']
db_user = config['db_user']
    
try:
    # Close previous connection
    if 'conn' in globals():
        conn.close()
        print("Closing connection")

    # Read from db_credentials.txt password required to connect to MongoDB.
    with open("db_credentials.txt", 'r') as f:
        [db_password] = f.read().splitlines()

    # Connect
    conn=pymongo.MongoClient("mongodb+srv://{}:{}@{}".format(db_user, db_password, db_url), ssl_cert_reqs=ssl.CERT_NONE)
    print ("Connected successfully to MongoDB")

except pymongo.errors.ConnectionFailure as e:
    print ("Could not connect to MongoDB: %s" % e) 

db = conn[db_name]

def get_similarity_row(simil_string, num_digits, movie_list):
    simil_row = []
    for i in range(len(movie_list)):
        x_char = simil_string[i*num_digits : (i+1)*num_digits]
        simil_row.append(int(x_char)/10**num_digits)  # Convert to number between 0 and 1
    return simil_row

# Collaborative filtering based similarity matrix
simMat_name = 'similarity_CF'
num_digits = 2
col_similarity = db[simMat_name]
CF_similarity = list(col_similarity.find())
CF_movies = np.array([movie['movieId'] for movie in CF_similarity])
CF_similarity = np.array([get_similarity_row(movie['similarities'], num_digits, CF_movies) for movie in CF_similarity])

# Content based similarity matrix
simMat_name = 'similarity_content_based'
num_digits = 4
col_similarity = db[simMat_name]
CB_similarity = list(col_similarity.find())
CB_movies = np.array([movie['movieId'] for movie in CB_similarity])
CB_similarity = np.array([get_similarity_row(movie['similarities'], num_digits, CB_movies) for movie in CB_similarity])

# Compute similarities

i_users = 1
all_users = all_ratings.userId.unique()

for user in tqdm(all_users): 
    i_users += 1
    input_movies = all_ratings.loc[(all_ratings.as_input & (all_ratings.userId == user)), 'movieId'].values
    input_ratings = all_ratings.loc[(all_ratings.as_input & (all_ratings.userId == user)), 'binary_rating'].values
    output_movies = all_ratings.loc[(~all_ratings.as_input & (all_ratings.userId == user)), 'movieId'].values

    input_idx = np.isin(CF_movies, input_movies)
    output_idx = np.isin(CF_movies, output_movies)
    similarity = CF_similarity[np.ix_(input_idx,output_idx)]
    # predCF = np.dot(input_ratings, similarity)/np.sum(similarity, axis=0)
    predCF = np.dot(input_ratings, similarity)/len(input_movies)
    all_ratings.loc[(~all_ratings.as_input & (all_ratings.userId == user)),'CF_prediction'] = predCF

    input_idx = np.isin(CB_movies, input_movies)
    output_idx = np.isin(CB_movies, output_movies)
    similarity = CB_similarity[np.ix_(input_idx,output_idx)]
    # predCB = np.dot(input_ratings, similarity)/np.sum(similarity, axis=0)
    predCB = np.dot(input_ratings, similarity)/len(input_movies)
    all_ratings.loc[(~all_ratings.as_input & (all_ratings.userId == user)),'CB_prediction'] = predCB

    if i_users%10000 == 0:
        # all_ratings.to_csv('/Users/irenebonafonte/Documents/MasterDS/AgileDS/GMAM_noGit/data_with_predRatings/binary2.5/ratings_split'+str(sys.argv[1])+'.csv')
        all_ratings.to_csv('/Users/irenebonafonte/Documents/MasterDS/AgileDS/GMAM_noGit/data_with_predRatings/unEscaled/ratings_split'+str(sys.argv[1])+'.csv')



