import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = " ".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    recommended_movies = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movie_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Select Movie', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, movie, poster in zip(cols, recommended_movie, recommended_movie_posters):
        col.text(movie)
        col.image(poster)