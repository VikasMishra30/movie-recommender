import streamlit as st
import pickle
import pandas as pd
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load sentiment analysis model and tokenizer
model = load_model("sentiment_analysis_model.h5")
with open("tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

# Function to predict sentiment
def predict_sentiment(review):
    sequence = tokenizer.texts_to_sequences([review])
    padded_sequence = pad_sequences(sequence, maxlen=200)
    prediction = model.predict(padded_sequence)
    sentiment = "positive" if prediction[0][0] > 0.5 else "negative"
    return sentiment

# Function to fetch the movie poster using TMDb API
def fetch_poster(movie_id):
    api_key = " "  # Replace with your TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if (poster_path):
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
    return None

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

# Movie recommendation section
selected_movie_name = st.selectbox('Select Movie', movies['title'].values)
if st.button('Show Recommendation'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for col, movie, poster in zip(cols, recommended_movies, recommended_movie_posters):
        col.text(movie)
        if poster:
            col.image(poster)
        else:
            col.text('No poster available')

# Sentiment analysis section
st.title('Sentiment Analysis of Movie Reviews')
user_review = st.text_area("Enter your movie review:")
if st.button('Predict Sentiment'):
    sentiment = predict_sentiment(user_review)
    st.write(f"The sentiment of the review is: {sentiment}")
