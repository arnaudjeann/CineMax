import requests


class APIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    def get_suggestions(self, query):
        """Fetch movie suggestions for the live search dropdown."""
        url = f"{self.base_url}/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
            "include_adult": "false",
            "language": "en-US"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('results', [])[:8]
        except Exception as e:
            print(f"DEBUG - Suggestion Error: {e}")
            return []

    def fetch_movie_details(self, title, year=None):
        """Fetch full movie data, cast, and crew for database import."""
        search_url = f"{self.base_url}/search/movie"
        params = {"api_key": self.api_key, "query": title, "year": year}

        try:
            response = requests.get(search_url, params=params)
            results = response.json().get('results')
            if not results: return None

            movie_id = results[0]['id']
            credits_url = f"{self.base_url}/movie/{movie_id}/credits"
            credits_response = requests.get(credits_url, params={"api_key": self.api_key})

            return {
                "info": results[0],
                "cast": credits_response.json().get('cast', [])[:5],
                "crew": credits_response.json().get('crew', [])
            }
        except Exception as e:
            print(f"DEBUG - Details Fetch Error: {e}")
            return None

    def get_trending_movies(self):
        """Fetch this week's top 20 trending movies."""
        url = f"{self.base_url}/trending/movie/week"
        try:
            response = requests.get(url, params={"api_key": self.api_key})
            return response.json().get('results', [])
        except Exception as e:
            print(f"DEBUG - Trending Error: {e}")
            return []