import pickle
import streamlit as st
import requests
import random
import pandas as pd

# Set page config
st.set_page_config(page_title="Cinematic Discoveries", page_icon="🎬", layout="wide")

# Advanced CSS with more animations and visual enhancements
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;400;700&display=swap');

        /* Cosmic Background Animation */
        body {
            background: linear-gradient(240deg, #1a1a2e, #16213e, #0f3460);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
            color: #e0e0f8;
            font-family: 'Roboto', sans-serif;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Starry Overlay Effect */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(white 1px, transparent 1px),
                radial-gradient(white 1px, transparent 1px);
            background-position: 0 0, 50px 50px;
            background-size: 100px 100px;
            opacity: 0.1;
            animation: moveStars 30s linear infinite;
            pointer-events: none;
            z-index: -1;
        }

        @keyframes moveStars {
            0% { background-position: 0 0, 50px 50px; }
            100% { background-position: 100px 100px, 150px 150px; }
        }

        /* Heading Animations */
        .main-heading {
            font-family: 'Orbitron', sans-serif;
            font-size: 4em;
            text-align: center;
            background: linear-gradient(90deg, #6a0dad, #8a2be2, #b19cd9, #da70d6);
            background-size: 300% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: shine 5s linear infinite;
        }

        @keyframes shine {
            to {
                background-position: 300% center;
            }
        }

        /* Movie Card Enhancements */
        .movie-card {
            perspective: 1500px;
            transition: all 0.7s cubic-bezier(0.455, 0.03, 0.515, 0.955);
            transform-style: preserve-3d;
        }

        .card-inner {
            position: relative;
            width: 100%;
            height: 400px;
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            border-radius: 15px;
            overflow: hidden;
        }

        .movie-card:hover .card-inner {
            transform: rotateY(180deg) rotateX(20deg);
        }

        .card-front, .card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: all 0.6s ease;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        }

        .card-front {
            background: linear-gradient(145deg, rgba(45,45,79,0.8), rgba(26,26,46,0.8));
            overflow: hidden;
        }

        .card-front img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s ease;
        }

        .movie-card:hover .card-front img {
            transform: scale(1.1) rotate(5deg);
        }

        .card-back {
            background: linear-gradient(145deg, #6a0dad, #8a2be2);
            transform: rotateY(180deg) rotateX(20deg);
            color: white;
            padding: 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: 'Orbitron', sans-serif;
        }

        .card-back h3 {
            font-size: 1.2em;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(255,255,255,0.5);
        }

        .card-back p {
            font-size: 0.9em;
            opacity: 0.8;
        }

        /* Button Styling */
        .stButton>button {
            background: linear-gradient(145deg, #6a0dad, #8a2be2);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 18px;
            border-radius: 15px;
            transition: all 0.4s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(106,13,173,0.4);
        }

        .stButton>button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(120deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: all 0.5s ease;
        }

        .stButton>button:hover {
            transform: scale(1.05) rotate(2deg);
            box-shadow: 0 15px 25px rgba(106,13,173,0.6);
        }

        /* Description Styling */
        .description {
            text-align: center;
            font-size: 1.2em;
            color: #bdb9d7;
            max-width: 800px;
            margin: 20px auto;
            line-height: 1.6;
            animation: fadeIn 1.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Footer Styling */
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 1em;
            color: #bdb9d7;
            opacity: 0.7;
            animation: pulse 2s infinite alternate;
        }

        @keyframes pulse {
            from { transform: scale(1); }
            to { transform: scale(1.05); }
        }
    </style>
""", unsafe_allow_html=True)

# Existing functions remain the same
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3e4e414eba32ce0c9136b9b0cc0f6315&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Create a more dynamic heading with added effects
st.markdown('''
    <h1 class="main-heading" style="margin-bottom: 20px;">
        🎬 Cinematic <span style="background: linear-gradient(90deg, #8a2be2, #da70d6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Discoveries</span>
    </h1>
''', unsafe_allow_html=True)

# Enhanced description with more dynamic text
st.markdown('''
    <p class="description" style="font-family: 'Orbitron', sans-serif;">
    🚀 Embark on a Cosmic Cinema Expedition | Intelligent Recommendations | Personalized Movie Universe
    </p>
    <p class="description" style="margin-top: 10px;">
    Dive into a cinematic journey that transcends ordinary recommendations. 
    Our AI-powered system curates a personalized movie experience, 
    unveiling hidden gems tailored just for you.
    </p>
''', unsafe_allow_html=True)

# Load data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Movie selection with enhanced dropdown
movie_list = movies['title'].values
default_movie = random.choice(movie_list)
selected_movie = st.selectbox(
    "🔍 Explore Your Next Cinematic Adventure", 
    movie_list,
    index=list(movie_list).index(default_movie)
)

# Enhanced Recommendation Button
if st.button('Unveil Cinematic Matches 🌟'):
    # Get recommendations
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display recommended movies with more context
    cols = st.columns(5)
    
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f'''
                <div class="movie-card">
                    <div class="card-inner">
                        <div class="card-front">
                            <img src="{recommended_movie_posters[idx]}" alt="Movie Poster">
                        </div>
                        <div class="card-back">
                            <h3>{recommended_movie_names[idx]}</h3>
                            <p>Similar to {selected_movie}</p>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

# Creator and Project Information Section
st.markdown('''
    <div style="text-align: center; margin-top: 40px; background: linear-gradient(145deg, rgba(106,13,173,0.2), rgba(138,43,226,0.2)); padding: 20px; border-radius: 15px;">
        <h2 style="color: #8a2be2; font-family: 'Orbitron', sans-serif;">🚀 Project Insights</h2>
        <p style="color: #bdb9d7; font-size: 1em;">
            Created with ❤️ by <span style="color: #6a0dad; font-weight: bold;">Yashvardhan Dhaka</span>
        </p>
        <p style="color: #e0e0f8; font-size: 0.9em; opacity: 0.8;">
            An intelligent movie recommendation system powered by machine learning
        </p>
    </div>
''', unsafe_allow_html=True)

# Additional Footer
st.markdown('''
    <p class="footer">
    Cinematic Discoveries © 2024 | Powered by Machine Learning 🤖✨
    </p>
''', unsafe_allow_html=True)