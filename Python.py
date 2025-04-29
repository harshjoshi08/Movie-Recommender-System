import streamlit as st 
import pickle
import pandas as pd
import numpy as np
import requests


# fetch poster function
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()  # Convert the response to JSON
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']  # Return the poster path from the JSON data


# Recommend function
def recommend(movie_name):
    movie_index = movies_list[movies_list['title'] == movie_name].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].movie_id  # Use the actual movie ID
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_list = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Streamlit App
st.title("Movie Recommender System")

Selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies_list['title'].values)

if st.button('Show Recommendation'):
    names, posters = recommend(Selected_movie_name)
    st.subheader("You may also like:")
    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
