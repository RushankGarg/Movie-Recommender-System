from urllib import response

import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
def fetch_poster(movie_id):
    response=requests.get(
    'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id)
    )
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']
def recommend(Selected_movie_name):
    movie_index = movies[movies['title'] == Selected_movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    movies_poster=[]
    for i in movies_list:
        movie_id=movies .iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]].title)
        movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,movies_poster
movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
movies_dict=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommendation System')
Selected_movie_name=st.selectbox('Select an option',movies['title'].values)
if st.button('Recommend'):
    names,posters= recommend(Selected_movie_name)
    col1, col2, col3, col4,col5 = st.columns(5)
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