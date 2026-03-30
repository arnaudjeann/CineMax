import requests
import os
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    def __init__(self):
        self.api_token = os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = {
            "Authorization" : f"Bearer {self.api_token}",
            "Content-Type": "application/json;charset=utf-8"
        }

    def fetch_movie_data(self, title, year=None):
        """Search for a movie and return its main data and credits."""
        search_url = f"{self.base_url}/search/movie"
        params = {"query": title, "year": year}

        response = requests.get(search_url, headers=self.headers, params=params)
        results = response.json().get('results')

        if not results:
            return None

        movie_id = results[0]['id']

        credits_url = f"{self.base_url}/movie/{movie_id}/credits"
        credits_response = requests.get(credits_url, headers=self.headers)
        credits_data = credits_response.json()

        return {
            "info": results[0],
            "cast": credits_data.get('cast', [])[:5],
            "crew": credits_data.get('crew', [])
        }

    def get_trending_movies(self):
        """ Fetches the top 20 trending movies of the week from TMBD."""
        url = f"{self.base_url}/trending/movie/week"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('results', [])
        except requests.exceptions.RequestException as e:
            print(f"API Error during trending fetch: {e}")
            return []