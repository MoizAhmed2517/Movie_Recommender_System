import streamlit as st
from movie_recommendersystem import newMoviesDf, resultant_vector
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=05420bcb8ec0e066754fc2a9fdf4a95e'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


st.title('Movie Recommender System')
movie_list = newMoviesDf['title'].values
select_movie_name = st.selectbox('Please select your favorite movie', movie_list)


def recommend(movie):
    movie_index = newMoviesDf[newMoviesDf['title'] == movie].index[0]
    distances = resultant_vector[movie_index]
    similarity = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in similarity:
        recommended_movies.append(newMoviesDf.iloc[i[0]].title)
        # fetching from API_key and movie_id
        recommended_movies_poster.append(fetch_poster(newMoviesDf.iloc[i[0]].movie_id))
    return recommended_movies, recommended_movies_poster


if st.button('Recommend'):
    names, posters = recommend(select_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
