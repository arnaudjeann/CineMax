from src.api_client import APIClient
from src.database import DatabaseManager

class DataProcessor:
    def __init__(self, api_key, db_name="cinemax.db"):
        self.db = DatabaseManager()
        self.api = APIClient(api_key)
        self.db.create_tables()

    def process_new_movie(self, raw_title, year=None):
        """The core logic: Search, Clean, and Link in Database."""
        data = self.api.fetch_movie_details(raw_title, year)
        if not data:
            print(f"Skipping {raw_title}: Not found on TMDB.")
            return

        movie_info = data['info']
        cast = data['cast']

        # 1. Find the director in the crew
        director_name = next((person['name'] for person in data['crew'] if person['job'] == 'Director'), "Unknown")

        # 2. Save to Database
        print(f"Processing: {movie_info['title']} by {director_name}")
        for actor in cast:
            print(f" - Adding actor: {actor['name']}")

    def process_file(self, raw_title, year=None):
        print(f"--- Processing: {raw_title} ---")

        # Fetch from API
        data = self.api.fetch_movie_details(raw_title, year)
        if not data:
            print(f"Could not find {raw_title} on TMDB.")
            return

        movie_info = data['info']
        cast = data['cast']

        # Find Director
        director = next((person['name'] for person in data['crew'] if person['job'] == 'Director'), "Unknown")

        #Save everything to SQL
        self.db.save_movie_with_relations(movie_info, director, cast)
        print(f"Successfully added {movie_info['title']} to your network.")