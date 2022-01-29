import pandas as pd
import numpy as np
import json
import pymongo
import ssl

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
    output_ratings1 = np.dot(input_ratings, similarity)/np.sum(similarity, axis=0)
    
    # Sort predictions by movie ID
    order = np.argsort(movie_list[sim_to_rate_bool].values.reshape(-1))
    output_ratings1 = output_ratings1[order]
    
    # If a movie has 0 similarity to all rated movies, give them a 0
    output_ratings1[np.isnan(output_ratings1)] = 0 
    
    return(output_ratings1)            


def combine_predictions(predCF, predCB):
    return (predCF + predCB)/2


def predictor(user_input, output_movies):
    # Extract rated movies Id and rating from input
    input_movies = [mov['movieId'] for mov in user_input] 
    input_ratings = [mov['valoration'] for mov in user_input]

    # Sort output movies by movie Id
    output_movies = np.sort(output_movies)
    
    # Exclude from output movies in input (already seen)
    output_movies = output_movies[~ np.isin(output_movies, input_movies)]
    
    # Predict using Collaborative filtering
    predCF = make_prediction(input_movies, input_ratings, output_movies, sim_mat_name='similarity_CF', sim_mat_digits=2)
    
    # Predict using Content Based recomender     
    predCB = make_prediction(input_movies, input_ratings, output_movies, sim_mat_name='similarity_content_based', sim_mat_digits=4)
    
    # Combine both predictions
    output_ratings = combine_predictions(predCF, predCB)

    # Sort predictions based on ratings
    output_movies = output_movies[np.argsort(-output_ratings)]
    
    return output_movies


# Example
with open('example_input.json', 'r') as fp:
    user_input = json.load(fp)

with open('example_output.json', 'r') as fp:
    user_output = json.load(fp)
    
output_movies = [899, 306, 1088, 2068]

sorted_movies = predictor(user_input, output_movies)