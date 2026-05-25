import requests

def get_movie_details(movie_title, api_key):

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        return {
            "poster": data.get("Poster", "N/A"),
            "rating": data.get("imdbRating", "N/A"),
            "year": data.get("Year", "N/A"),
            "plot": data.get("Plot", "Plot not available"),
            "title": data.get("Title", movie_title)
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "poster": "N/A",
            "rating": "N/A",
            "year": "N/A",
            "plot": "Plot not available",
            "title": movie_title
        }