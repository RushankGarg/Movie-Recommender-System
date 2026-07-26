import streamlit as st
import pickle
import pandas as pd
import requests
import time




def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": "f77e757c1f04b7fd1b2235380609b168",
        "language": "en-US"
    }

    # Try up to 3 times if connection fails
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

            return None

        except requests.exceptions.RequestException as e:
            print(f"TMDB request failed: {e}")

            if attempt < 2:
                time.sleep(2)

    return None




def recommend(selected_movie_name):

    movie_index = movies[
        movies["title"] == selected_movie_name
    ].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    movie_posters = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]]["movie_id"]

        recommended_movies.append(
            movies.iloc[i[0]]["title"]
        )

        movie_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, movie_posters




movie_data = pickle.load(
    open("movie_dict.pkl", "rb")
)

movies = pd.DataFrame(movie_data)

similarity = pickle.load(
    open("similarity.pkl", "rb")
)


# -------------------------------
# Streamlit UI
# -------------------------------

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)


if st.button("Recommend"):

    with st.spinner("Finding recommendations..."):

        names, posters = recommend(
            selected_movie_name
        )

    cols = st.columns(5)

    for i, col in enumerate(cols):

        with col:

            st.text(names[i])

            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster unavailable")
