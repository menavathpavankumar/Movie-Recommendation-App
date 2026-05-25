# main.py

import json
import streamlit as st
from recommend import df, recommend_movies
from recommend import df, recommend_movies
from omdb_utils import get_movie_details

# Load config
with open("src/config.json", "r") as file:
    config = json.load(file)

OMDB_API_KEY = config["OMDB_API_KEY"]

# Streamlit page settings
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Title
st.title("🎬 Movie Recommender System")
st.write("Discover similar movies with posters, ratings and plots.")

# Movie dropdown
movie_list = sorted(df['title'].dropna().unique())

selected_movie = st.selectbox(
    "🎥 Select a Movie",
    movie_list
)

# Button
if st.button("🚀 Recommend Movies"):

    recommendations = recommend_movies(selected_movie)

    if recommendations is None or recommendations.empty:
        st.warning("No recommendations found.")

    else:
        st.success("✅ Top Similar Movies")

        for _, row in recommendations.iterrows():

            movie_title = row['title']

            # Get movie details from API
            details = get_movie_details(movie_title, OMDB_API_KEY)

            # Safety check
            if details is None:
                details = {
                    "poster": "N/A",
                    "rating": "N/A",
                    "year": "N/A",
                    "plot": "Plot not available",
                    "title": movie_title
                }

            poster = details.get("poster", "N/A")
            rating = details.get("rating", "N/A")
            year = details.get("year", "N/A")
            plot = details.get("plot", "Plot not available")
            title = details.get("title", movie_title)

            st.markdown("---")

            col1, col2 = st.columns([1, 3])

            # Poster
            with col1:

                if poster != "N/A":
                    st.image(poster, width=200)

                else:
                    st.write("❌ No Poster Found")

            # Movie details
            with col2:

                st.markdown(f"## {title}")

                st.write(f"⭐ IMDb Rating: {rating}")

                st.write(f"📅 Release Year: {year}")

                st.write(f"📝 Overview: {plot}")