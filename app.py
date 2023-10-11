import streamlit as st
import json
import base64 
from classifier import KNearestNeighbours
from operator import itemgetter
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    song_titles = json.load(f)

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack('pexels-daniel-reche-3721941 (1).jpg')


def knn(test_point, k):
    
    target = [0 for item in song_titles]
    
    model = KNearestNeighbours(data, target, test_point, k=k)
  
    model.fit()
    
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    
    table = list()
    for i in model.indices:
        
        table.append([song_titles[i][0], song_titles[i][2]])
    return table

if __name__ == '__main__':
    genres = ['Sufi',
 'dance',
 'dark',
 'happy',
 'hip hop',
 'motivational',
 'party',
 'pop',
 'rap',
 'rock',
 'romantic',
 'sad',
 'slow']

    SONGS = [title[0] for title in song_titles]
    st.header('RYTHM') 
    apps = ['--Select--', 'Song based', 'Mood based']   
    app_options = st.selectbox('Select application:', apps)
    
    if app_options == 'Song based':
        song_select = st.selectbox('Select song:', ['--Select--'] + SONGS)
        if song_select == '--Select--':
            st.write('Select a song')
        else:
            n = st.number_input('Number of songs:', min_value=1, max_value=20, step=1)
            var = data[SONGS.index(song_select)]
            test_point = var
            table = knn(test_point, n)
            for song, link in table:
                
                st.markdown(f"[{song}]({link})")
    elif app_options == apps[2]:
        options = st.multiselect('Select genres:', genres)
        if options:
        
            n = st.number_input('Number of songs:', min_value=1, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
         
            table = knn(test_point, n)
            for i, link in table:
                
                st.markdown(f"[{i}]({link})")

        else:
                st.write("This is a simple SONG Recommender application. "
                        "You can select the genres and get recommendations")

    else:
        st.write('Select option')