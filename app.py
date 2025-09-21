import pickle
import streamlit as st
import requests
import pandas as pd

st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Fetch poster from TMDb
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_links = []

    for i in distances:
        movie_id = movies.iloc[i[0]]['id']   # use correct column for TMDb ID
        recommended_movie_names.append(movies.iloc[i[0]]['title'])
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_links.append(f"https://www.themoviedb.org/movie/{movie_id}")

    return recommended_movie_names, recommended_movie_posters, recommended_movie_links

# Show recommendations
if st.button('Show Recommendation'):
    names, posters, links = recommend(selected_movie)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            # Use markdown for clickable image
            st.markdown(f"[![{names[i]}]({posters[i]})]({links[i]})")
            st.text(names[i])
