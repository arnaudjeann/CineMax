from flask import Flask, render_template, request
from werkzeug.utils import redirect
from src.database import DatabaseManager
from src.api_client import APIClient
from src.processor import DataProcessor

app = Flask(__name__)
db = DatabaseManager("cinemax.db")
api_client = APIClient()
processor = DataProcessor("cinemax.db")

@app.route('/')
def index():
    all_movies = db.get_all_movies()

    return render_template('index.html', movies_list=all_movies)

@app.route('/search', methods=['POST'])
def search_connection():
    movie1 = request.form.get('movie1')
    movie2 = request.form.get('movie2')

    shared_actors = db.find_shared_actors(movie1, movie2)
    all_movies = db.get_all_movies()

    return render_template('index.html',
                           actors=shared_actors,
                           m1=movie1,
                           m2=movie2,
                           movies_list=all_movies)

@app.route('/import', methods=['POST'])
def import_movie():
    movie_title = request.form.get('new_movie')
    from src.processor import DataProcessor
    processor = DataProcessor()

    processor.process_file(movie_title, "")

    return redirect('/')

@app.route('/sync-trending')
def sync_trending():
    try:
        trending_movies = api_client.get_trending_movies()
        for movie in trending_movies:
            title = movie.get('title')
            release_date = movie.get('release_date', '')
            year = release_date[:4] if release_date else ""
            processor.process_file(title, year)
        return redirect('/')
    except Exception as e:
        print(f"Synchronization erreor: {e}")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)