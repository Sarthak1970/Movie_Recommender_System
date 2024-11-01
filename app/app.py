import streamlit as st
import pandas as pd
import pickle
import requests

api_key='6bfd2fe06bec25cd3067c4d69f7aaf26'

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    data = response.json()
    
    # Check if 'poster_path' is None
    if data.get('poster_path') is not None:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # Return a default image URL if the poster_path is None
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]]['title'])
        #fetch poster
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie=st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters=recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
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

