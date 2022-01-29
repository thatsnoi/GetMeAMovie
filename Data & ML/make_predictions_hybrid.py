import pandas as pd
import numpy as np
import json
import pymongo
import ssl
from joblib import dump, load
from sklearn.ensemble import GradientBoostingRegressor
import math

def get_similarity_row(movieId, db_connection, db_name, simMat_name, movie_list, num_digits=2):
    '''Obtain similarities of selected movie (will give error if movieId does not exist)'''
    db = db_connection[db_name]
    col_similarity = db[simMat_name]
    simil_string = col_similarity.find({'movieId':movieId})[0]['similarities']
    simil_row = []
    for i in range(len(movie_list)):
        x_char = simil_string[i*num_digits : (i+1)*num_digits]
        simil_row.append(int(x_char)/10**num_digits)  # Convert to number between 0 and 1
    return simil_row


def get_similarity(input_movies, sim_mat_name, sim_mat_digits):
    # Read configuration file
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
    
    # Open database and collection
    db = conn[db_name]
    col_similarity = db[sim_mat_name]

    # Read movie ids from DB into a dataframe
    movie_list = pd.DataFrame(list(col_similarity.find( {}, {'movieId':1, '_id':0} )))

    # Read similarity matrix
    similarity = np.array([get_similarity_row(i, conn, db_name, sim_mat_name, movie_list, sim_mat_digits) for i in input_movies])

    return(movie_list, similarity)


def make_prediction(input_movies, input_ratings, output_movies, sim_mat_name='similarity_CF', sim_mat_digits=2):
    # Get similarity matrix for seen movies
    movie_list, similarity = get_similarity(input_movies, sim_mat_name, sim_mat_digits)
    
    # Subset to similarity matrix with movies to be rated
    sim_to_rate_bool = movie_list.isin(output_movies).values.reshape(-1)
    similarity = similarity[:,sim_to_rate_bool]
    
    # Compute predictions
    output_ratings1 = np.dot(input_ratings, similarity)/len(input_movies)
    
    # Sort predictions by movie ID
    order = np.argsort(movie_list[sim_to_rate_bool].values.reshape(-1))
    output_ratings1 = output_ratings1[order]
    
    # If a movie has 0 similarity to all rated movies, give them a 0
    output_ratings1[np.isnan(output_ratings1)] = 0 
    
    return(output_ratings1)            


def combine_predictions(predCF, predCB, user_input, user_output):
    
    # Load the model 
    regr = load('GBR100.joblib') 
    
    # Other necessary parameters
    genres = ['no_genres', 'action', 'adventure', 'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy',
              'film-noir', 'horror', 'imax', 'musical', 'mystery', 'romance', 'sci-fi', 'thriller', 'war', 'western']

    directors = ['Alfred Hitchcock', 'Andrew Davis', 'Andrew Stanton', 'Barry Levinson', 'Barry Sonnenfeld', 'Brian De Palma', 'Bryan Singer', 'Chris Columbus',
           'Christopher Nolan', 'David Fincher', 'Francis Ford Coppola', 'Frank Darabont', 'George Lucas', 'James Cameron', 'Jan de Bont', 'Joel Coen',
           'Joel Schumacher', 'John McTiernan', 'Jonathan Demme', 'Lilly Wachowski', 'Martin Scorsese', 'Mel Gibson', 'Michael Bay', 'Peter Jackson',
           'Quentin Tarantino', 'Richard Donner', 'Ridley Scott', 'Rob Reiner', 'Robert Zemeckis', 'Roland Emmerich', 'Ron Howard', 'Sam Mendes',
           'Stanley Kubrick', 'Steven Spielberg', 'Terry Gilliam', 'Tim Burton', 'Tom Shadyac', 'Tony Scott', 'Wolfgang Petersen']

    directors2 = ['Steven Spielberg', 'Robert Zemeckis', 'Christopher Nolan', 'James Cameron', 'Quentin Tarantino', 'Peter Jackson', 'David Fincher', 'Ridley Scott',
           'Martin Scorsese', 'Tim Burton', 'Ron Howard', 'Frank Darabont', 'Francis Ford Coppola', 'George Lucas', 'Stanley Kubrick',
           'John McTiernan', 'Roland Emmerich', 'Chris Columbus', 'Jonathan Demme', 'Rob Reiner', 'Bryan Singer', 'Terry Gilliam', 'Joel Coen',
           'Lilly Wachowski', 'Barry Sonnenfeld', 'Alfred Hitchcock', 'Joel Schumacher', 'Tom Shadyac', 'Wolfgang Petersen', 'Jan de Bont',
           'Tony Scott', 'Richard Donner', 'Michael Bay', 'Mel Gibson', 'Brian De Palma', 'Andrew Stanton', 'Sam Mendes', 'Andrew Davis', 'Barry Levinson']

    # Codify input movies stats
    df = user_input
    input_stats = []
    for rate in [1, -1]:

        partial_stats = [len(df), np.std(df.year), np.std(df.num_ratings), np.std(df.avg_rating), np.std(df.runtimeMinutes), np.mean(df.year), 
                 np.mean(df.num_ratings), np.mean(df.avg_rating), np.sum(df.isAdult), np.mean(df.runtimeMinutes)]

        input_genres = np.array([item for sub_list in df.genres.values for item in sub_list])
        n_genres = [np.sum(input_genres == genre) for genre in genres]
        n_directors = [np.sum(df.director == director) for director in directors2]

        input_stats = input_stats + partial_stats + n_genres + n_directors


    # Codify output movies stats
    df = pd.concat([pd.DataFrame({'CF_prediction': predCF, 'CB_prediction': predCB}), user_output], axis=1)
    df = scale(df)
    output_genres = df.genres.values
    df.drop('genres',axis=1,inplace=True)
    df[genres] = 0
    df[directors] = 0
    df.loc[~df.director.isin(directors),'director'] = ''
    
    for i in range(len(df)):
        dirr = df.director[i]
        if dirr != '':
            df[dirr][i] = df[dirr][i] + 1
        
        #print(df.movieId[i], i, output_genres[i])
        for genre in output_genres[i]:   
            df[genre][i] = 1
        #else:
        #    df['no_genres'][i] = 1
            
    df.drop(['movieId','director'], axis=1, inplace=True)   
    df = df.to_numpy()
    input_stats = np.tile(np.array(input_stats), (df.shape[0], 1))

    df = np.concatenate((df, input_stats), axis=1)
    
    # Make predictions
    predictions = regr.predict(df)

    return predictions

def scale(df):
    minv = min(df.CF_prediction)
    maxv = max(df.CF_prediction)
    df.loc[np.isnan(df.CF_prediction),'CF_prediction'] = 0
    df.CF_prediction = 5*(df.CF_prediction - minv)/(maxv - minv)
    
    minv = min(df.CB_prediction)
    maxv = max(df.CB_prediction)
    df.CB_prediction = 5*(df.CB_prediction - minv)/(maxv - minv)   
    df.loc[np.isnan(df.CB_prediction),'CB_prediction'] = 0
    
    return df

def predictor(user_input, user_output):
    # Extract rated movies Id and rating from input
    input_movies = [mov['movieId'] for mov in user_input] 
    input_ratings = [mov['valoration'] for mov in user_input]
    user_input = pd.DataFrame(user_input)

    # Sort output movies by movie Id
    output_movies = [mov['movieId'] for mov in user_output] 
    output_movies = np.sort(output_movies)
    
    # Exclude from output movies in input (already seen)
    user_output = pd.DataFrame(user_output)
    user_output = user_output.loc[~ np.isin(output_movies, input_movies),:]
    user_output.reset_index(inplace=True, drop=True)
    output_movies = output_movies[~ np.isin(output_movies, input_movies)]
    
    # Predict using Collaborative filtering
    predCF = make_prediction(input_movies, input_ratings, output_movies, sim_mat_name='similarity_CF', sim_mat_digits=2)
    
    # Predict using Content Based recomender     
    predCB = make_prediction(input_movies, input_ratings, output_movies, sim_mat_name='similarity_content_based', sim_mat_digits=4)
    
    # Combine both predictions
    output_ratings = combine_predictions(predCF, predCB, user_input, user_output)

    # Sort predictions based on ratings
    output_movies = output_movies[np.argsort(-output_ratings)]
    
    return output_movies


# Example
with open('example_input.json', 'r') as fp:
    user_input = json.load(fp)

with open('example_output.json', 'r') as fp:
    user_output = json.load(fp)
    
sorted_movies = predictor(user_input, user_output)


