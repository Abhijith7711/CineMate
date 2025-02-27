#importing required libraries

import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process
import base64

# Set Page Configuration
st.set_page_config(
    page_title="CineMate",
    page_icon="🎬",
    layout="wide"
)

# Function to Convert Image to Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to Apply Custom Styling & Background
def set_background(image_path):
    base64_img = get_base64_image(image_path)
    bg_style = f"""
    <style>
        /* Background Styling */
        .stApp {{
            background: url("data:image/jpg;base64,{base64_img}") no-repeat center center fixed;
            background-size: cover;
        }}
        

        /* Force sidebar text to be black */
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] label {{
        color: black !important;
         }}


        /* White Text Styling */
        h1, h2, h3, h4, h5, h6, label, .stMarkdown {{
            color: white !important;
        }}

        /* Red Button for "Find Similar Movies" */
        div.stButton > button {{
            background-color: red !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            transition: 0.3s;
        }}

        div.stButton > button:hover {{
            background-color: darkred !important;
        }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# Apply Background
set_background("bg.png")  # Update with your image path

# Load Data and Models
@st.cache_data
def load_data():
    return pd.read_csv("moviedf.csv")

@st.cache_data
def load_models():
    tfidf_matrix = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
    cosine_sim = pickle.load(open("cosine_similarity.pkl", "rb"))
    return tfidf_matrix, cosine_sim

# Load datasets
movie = load_data()
tfidf_matrix, cosine_sim = load_models()

# Function to find the closest movie match
def find_best_match(input_movie):
    movie_names = movie['name'].tolist()
    best_match, score, _ = process.extractOne(input_movie, movie_names)
    return best_match, score

# Recommendation Function
def recommend_movies(movie_name, num_recommendations=5):
    if movie_name not in movie['name'].values:
        return None

    idx = movie[movie['name'] == movie_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations+1]

    movie_indices = [i[0] for i in sim_scores]
    return movie[['name', 'description', 'language', 'genre', 'cast']].iloc[movie_indices]

# Initialize session state
if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Settings")
    num_recommendations = st.slider("Number of Recommendations", 1, 10, 5)

# 🎬 **Main App**
st.title("🎬 CineMate")
st.markdown("#### Discover movies similar to your favorites!")

# Categorizing movies by language
languages = ["All", "Hindi", "Malayalam", "Tamil", "Telugu", "Panjabi"]
selected_language = st.selectbox("🎭 **Choose a Movie Language:**", languages)

# Filtering movies based on the selected language
filtered_movies = movie["name"].unique() if selected_language == "All" else movie[movie["language"] == selected_language]["name"].unique()

# **Movie Selection Input + Dropdown List**
col1, col2 = st.columns([3, 2])

with col1:
    movie_name = st.text_input("🎥 **Enter your favorite Movie:**")

with col2:
    selected_movie_from_list = st.selectbox("📜 **Or Select from List:**", sorted(filtered_movies))

# Assign the selected movie based on user input
final_movie_selection = movie_name.strip() if movie_name.strip() else selected_movie_from_list

# Button to find similar movies
if st.button("Find Similar Movies"):
    if not final_movie_selection:
        st.warning("⚠️ Please enter or select a movie.")
    else:
        best_match, score = find_best_match(final_movie_selection)

        if best_match and score < 80:
            st.error(f"❌ No close match found for '{final_movie_selection}'. Please try again.")
        else:
            st.session_state.selected_movie = best_match
            if best_match != final_movie_selection:
                st.info(f"🔍 Did you mean **'{best_match}'**?")

# Show recommendations inside a container
if st.session_state.selected_movie:
    recommendations = recommend_movies(st.session_state.selected_movie, num_recommendations)

    if recommendations is not None:
        with st.container():  # Creates a proper container around all recommendations
            st.markdown(
                """
                <div style="background-color: rgba(20, 20, 20, 0.8); padding: 15px; border-radius: 10px;">
                """,
                unsafe_allow_html=True,
            )

            st.success(f"✅ Movies similar to **{st.session_state.selected_movie}**:")

            for _, row in recommendations.iterrows():
                st.markdown(
                    f"""
                    <div style="background-color: rgba(40, 40, 40, 0.9); padding: 10px; margin-bottom: 10px; border-radius: 8px;">
                        <h4 style="color: white;">🎥 {row['name']}</h4>
                        <p style="color: white;"><b>🗣 Language:</b> {row['language']}  |  <b>🎭 Genre:</b> {row['genre']}</p>
                        <p style="color: white;"><b>👨‍🎤 Cast:</b> {row['cast']}</p>
                        <p style="color: white;"><b>📖 Description:</b> {row['description']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)  # Close the main container div
    else:
        st.error(f"❌ Movie '{st.session_state.selected_movie}' not found in the database.")
