import streamlit as slt
import pickle as pkl
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=" \
          "8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = []
    recommended_movies_posters = []
    for m in movies_list:
        # fetch the movie poster from api
        movie_id = movies.iloc[m[0]].movie_id

        recommended_movies.append(movies.iloc[m[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


movies_dict = pkl.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pkl.load(open('similarity.pkl', 'rb'))

slt.title('Movie Recommender System')

selected_movie_name = slt.selectbox('Hey! Search your Movie',
                                    movies['title'].values)

if slt.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    i = 0
    col1, col2, col3, col4, col5 = slt.columns(5)
    col6, col7, col8, col9, col10 = slt.columns(5)
    for col in [col1, col2, col3, col4, col5]:
        with col:
            slt.text(names[i])
            slt.image(posters[i])
            i += 1
    for col in [col6, col7, col8, col9, col10]:
        with col:
            slt.text(names[i])
            slt.image(posters[i])
            i += 1

    # col1, col2, col3, col4, col5 = slt.columns(5)
    # with col1:
    #     slt.text(names[0])
    #     slt.image(posters[0])
    # with col2:
    #     slt.text(names[1])
    #     slt.image(posters[1])
    #
    # with col3:
    #     slt.text(names[2])
    #     slt.image(posters[2])
    # with col4:
    #     slt.text(names[3])
    #     slt.image(posters[3])
    # with col5:
    #     slt.text(names[4])
    #     slt.image(posters[4])
