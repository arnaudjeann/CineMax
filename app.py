import os
import sqlite3

from flask import Flask, render_template, request, jsonify, redirect
from src.database import DatabaseManager
from src.api_client import APIClient
from src.processor import DataProcessor

# Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
app = Flask(__name__)

# Object Initialization
api_client = APIClient(TMDB_API_KEY)
db = DatabaseManager("cinemax.db")
processor = DataProcessor(TMDB_API_KEY, db)


@app.route('/')
def index():
    movies = db.get_all_movies()
    return render_template('index.html', movies_list=movies)


@app.route('/search-suggestions')
def search_suggestions():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify({"results": []})

    raw_results = api_client.get_suggestions(query)

    # Format data for the frontend
    suggestions = []
    for movie in raw_results:
        suggestions.append({
            "title": movie.get("title"),
            "poster_path": movie.get("poster_path"),
            "release_date": movie.get("release_date", "")
        })
    return jsonify({"results": suggestions})


@app.route('/import', methods=['POST'])
def import_movie():
    title = request.form.get('new_movie')
    if title:
        processor.process_file(title, "")
    return redirect('/')


@app.route('/sync-trending')
def sync_trending():
    trending = api_client.get_trending_movies()
    for movie in trending:
        processor.process_file(movie.get('title'), movie.get('release_date', '')[:4])
    return redirect('/')


@app.route('/search', methods=['POST'])
def search():
    movie1 = request.form.get('movie1')
    movie2 = request.form.get('movie2')

    shared_actors = db.find_shared_actors(movie1, movie2)

    all_movies = db.get_all_movies()

    return render_template('index.html',
                           actors=shared_actors,
                           m1=movie1,
                           m2=movie2,
                           movies_list=all_movies)

if __name__ == '__main__':
    app.run(debug=True)