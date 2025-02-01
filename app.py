import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import streamlit as st
import requests


im = Image.open("favicon.ico")
st.set_page_config(
    page_title="mrs",
    page_icon=im,
    layout="wide",
)
def fetch_trailer(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=af1d1e85e35255da989b33eaf4f5f47d")
    data = response.json()
    for i in data["results"]:
        if i["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={i['key']}"
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=af1d1e85e35255da989b33eaf4f5f47d")
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
def recommend(movie,similarity):
    movie_index = movies[movies["title"] == movie].index[0]
    distances  = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]
    recommended_movies = []
    trailer = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        trailer.append(fetch_trailer(movie_id))
        #fetch poster from api]
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster,trailer
st.title('Movie Recommendation System')
movies_list = pickle.load(open("movies_dict.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl",'rb'))
movies = pd.DataFrame(movies_list)
movie_name = st.selectbox("Which movie you want recommendations for",movies['title'].values)


if st.button("Recommend"):

    names, posters, trailers = recommend(movie_name, similarity)
    st.write("Click to View trailer!")
    # Create columns
    columns = st.columns(5)

    # Loop through columns and data
    for i, col in enumerate(columns):
        with col:
            st.markdown(f"""
            <a href="{trailers[i]}" target="_blank">
                <img src="{posters[i]}" alt="{names[i]}" style="width:100%; border-radius:10px;">
            </a>
            <p style="text-align:center; font-size:14px;">{names[i]}</p>
            """, unsafe_allow_html=True)

