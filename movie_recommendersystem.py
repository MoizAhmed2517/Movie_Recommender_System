import numpy as np
import pandas as pd
import ast

import streamlit
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

finalDataset = movies.merge(credits, on="title")

movies = finalDataset[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

movies.dropna(inplace=True)

newMoviesList = []
ps = PorterStemmer()


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


def convert(obj):
    MoviesList = []
    for i in ast.literal_eval(obj):
        MoviesList.append(i['name'])
    return MoviesList


def converCast(obj):
    newMoviesList = []
    for i in ast.literal_eval(obj):
        newMoviesList.append(i['name'])
    del newMoviesList[3:]
    return newMoviesList


def fethcDirector(obj):
    dirName = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            dirName.append(i['name'])
            break
    return dirName


movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(converCast)
movies['crew'] = movies['crew'].apply(fethcDirector)
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['tags'] = movies['overview'] + movies['genres'] + movies['cast'] + movies['cast'] + movies['crew'] + movies[
    'keywords']
newMoviesDf = movies[['movie_id', 'title', 'tags']]
newMoviesDf['tags'] = newMoviesDf['tags'].apply(lambda x: " ".join(x))
newMoviesDf['tags'] = newMoviesDf['tags'].apply(lambda x: x.lower())
newMoviesDf['tags'] = newMoviesDf['tags'].apply(stem)
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(newMoviesDf['tags']).toarray()
resultant_vector = cosine_similarity(vectors)


def recommend(movie):
    movie_index = newMoviesDf[newMoviesDf['title'] == movie].index[0]
    distances = resultant_vector[movie_index]
    similarity = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in similarity:
        print(newMoviesDf.iloc[i[0]].title)
