# 🎬 CineMate - Movie Recommendation System

[CineMate Live Demo](https://cinemate1.streamlit.app/) 🎥

## About
CineMate is a **content-based movie recommendation system** designed specifically for **Indian movies**. It helps users discover similar movies based on their preferences using **cosine similarity**. The recommendations are based on various attributes such as **movie descriptions, language, genre, cast, writer, and director**.

## Features
- 🔍 **Find Similar Movies**: Get personalized recommendations for Indian movies.
- 📌 **Multiple Language Support**: Filter movies based on languages like Hindi, Malayalam, Tamil, Telugu, and Punjabi.
- 🎭 **Content-Based Recommendations**: Uses movie descriptions and metadata for accurate suggestions.
  

## How It Works
1. Enter a movie name or select from the dropdown.
2. The system finds the best-matching movie using **rapidfuzz**.
3. Recommendations are generated based on **cosine similarity**.
4. Results display movie details, including genre, cast, and description.

## Technologies Used
- **Python** 
- **Streamlit** 
- **Pandas** 
- **Scikit-Learn** 
- **RapidFuzz** 
- **Pickle** 

## Installation & Running Locally
```sh
# Clone the repository
git clone https://github.com/yourusername/CineMate.git
cd CineMate

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deployment
The app is live on **Streamlit Cloud**: [CineMate](https://cinemate1.streamlit.app/).


