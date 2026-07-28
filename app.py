import streamlit as st
import pickle
import pandas as pd
import requests
import time



st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)



# API key comes from:
# .streamlit/secrets.toml
API_KEY = st.secrets["TMDB_API_KEY"]

TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie/{}"

TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

FALLBACK_POSTER = (
    "https://placehold.co/500x750"
    "?text=Poster+Unavailable"
)




def fetch_poster(movie_id):

    url = TMDB_MOVIE_URL.format(movie_id)

    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    # Retry 3 times if connection fails
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

            # Poster exists
            if poster_path:

                return (
                    TMDB_IMAGE_URL
                    + poster_path
                )

            # Movie exists but poster doesn't
            return FALLBACK_POSTER


        except requests.exceptions.Timeout:

            print(
                f"Timeout for movie {movie_id}. "
                f"Attempt {attempt + 1}/3"
            )


        except requests.exceptions.ConnectionError:

            print(
                f"Connection error for movie {movie_id}. "
                f"Attempt {attempt + 1}/3"
            )


        except requests.exceptions.HTTPError as e:

            print(
                f"HTTP error for movie {movie_id}: {e}"
            )

            return FALLBACK_POSTER


        except requests.exceptions.RequestException as e:

            print(
                f"Request error for movie {movie_id}: {e}"
            )

            return FALLBACK_POSTER


        # Wait before trying again
        if attempt < 2:

            time.sleep(2)


    return FALLBACK_POSTER




try:



    with open("movie_dict.pkl", "rb") as f:

        movie_data = pickle.load(f)


    movies = pd.DataFrame(movie_data)




    with open("similarity_small.pkl", "rb") as f:

        similarity = pickle.load(f)




except FileNotFoundError as e:

    st.error(
        f"Required file not found: {e}"
    )

    st.stop()




except EOFError:

    st.error(
        "One of the pickle files is empty or corrupted. "
        "Please recreate movie_dict.pkl or "
        "similarity_small.pkl."
    )

    st.stop()




except Exception as e:

    st.error(
        f"Error loading recommendation files: {e}"
    )

    st.stop()




def recommend(selected_movie_name):


    movie_match = movies[
        movies["title"] == selected_movie_name
    ]


    if movie_match.empty:

        return [], []



    movie_index = movie_match.index[0]




    try:

        recommended_indices = similarity[
            movie_index
        ]

    except KeyError:

        st.error(
            "Recommendation data not found "
            "for this movie."
        )

        return [], []


    recommended_movies = []

    movie_posters = []




    for index in recommended_indices:

        movie_id = movies.iloc[index][
            "movie_id"
        ]

        movie_title = movies.iloc[index][
            "title"
        ]


        recommended_movies.append(
            movie_title
        )


        poster = fetch_poster(
            movie_id
        )


        movie_posters.append(
            poster
        )


    return recommended_movies, movie_posters




st.title(
    "🎬 Movie Recommendation System"
)


st.write(
    "Select a movie to discover 5 similar movies."
)




selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)




if st.button(
    "Recommend",
    type="primary"
):

    with st.spinner(
        "Finding recommendations..."
    ):

        names, posters = recommend(
            selected_movie_name
        )




    if names:

        st.subheader(
            "Recommended Movies"
        )


        columns = st.columns(
            len(names)
        )


        for i, column in enumerate(columns):

            with column:

                st.markdown(
                    f"### {names[i]}"
                )


                st.image(
                    posters[i],
                    use_container_width=True
                )


    else:

        st.warning(
            "No recommendations found."
        )