import streamlit as st
import pickle
import pandas as pd
import requests

movies_lst = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_lst)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_movie(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

def recommendation(movie):
    name_lst = []
    poster_lst = []
    indexs = movies[movies['title'] == movie].index[0]
    distances = similarity[indexs]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    for i in movie_list:
        name_lst.append(movies.iloc[i[0]].title)
        poster_lst.append(fetch_movie(movies.iloc[i[0]].movie_id))
    return name_lst, poster_lst
st.title('Movie Recommendation System')

option = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
    movie_name, movie_poster = recommendation(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
