import streamlit as st
import pickle
import requests
import os

movies = pickle.load((open("movies_list.pkl", "rb")))
similarity = pickle.load((open("similarity.pkl", "rb")))
movies_list=movies['title'].values

st.header("Movie Recommending System")

selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def get_poster(movie_id):
    api_key = "3c97ffe6a040517e18ab492c667a5f7e"
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, api_key)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movies=[]
    recommend_posters=[]
    for i in distance[1:6]:
        movie_id=movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(get_poster(movie_id))
    return recommend_movies, recommend_posters

if st.button("Show recommend"):
    movie_name, movie_posters = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_posters[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_posters[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_posters[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_posters[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_posters[4])

