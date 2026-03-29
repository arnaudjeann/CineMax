import sqlite3

class DatabaseManager:
    def __init__(self, db_name="cinemax.db"):
        self.db_name = db_name

    def create_tables(self):
        """Initializes the relational structures of CineGraph."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # 1. Directors Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS directors (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE)''')

            # 2. Movie Table (linked to Director)
            cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                year INTEGER,
                                director_id INTEGER,
                                overview TEXT,
                                FOREIGN KEY (director_id) REFERENCES directors (id))''')

            # 3. Actors Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS actors (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE)''')

            # 4. Junction Table (Many-to-Many: Movies <-> Actors)
            cursor.execute('''CREATE TABLE IF NOT EXISTS movie_cast (
                                movie_id INTEGER,
                                actor_id INTEGER,
                                PRIMARY  KEY (movie_id, actor_id),
                                FOREIGN KEY (movie_id) REFERENCES movies (id),
                                FOREIGN KEY (actor_id) REFERENCES actors (id))''')

            conn.commit()
            print("Database initialized successfully.")

    def save_movie_with_relations(self, movie_data, director_name, cast_list):
        """High-level method to save a movie and its network or actors."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            # 1. Handle Director (Insert if not exists, then get ID)
            cursor.execute("INSERT OR IGNORE INTO directors (name) VALUES (?)", (director_name,))
            cursor.execute("SELECT id FROM directors WHERE name = ?", (director_name,))
            director_id = cursor.fetchone()[0]

            # 2. Insert Movie
            cursor.execute("""
                INSERT OR IGNORE INTO movies (title, year, director_id, overview)
                VALUES (?, ?, ?, ?)""",
                (movie_data['title'], movie_data['release_date'][:4], director_id, movie_data['overview'])
            )
            movie_id = cursor.lastrowid

            # 3. Handle Actors and Junction Table
            for actor in cast_list:
                cursor.execute("INSERT OR IGNORE INTO actors (name) VALUES (?)", (actor['name'],))
                cursor.execute("SELECT id FROM actors WHERE name = ?", (actor['name'],))
                actor_id = cursor.fetchone()[0]

                cursor.execute("INSERT OR IGNORE INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
                               (movie_id, actor_id))

            conn.commit()

    def find_shared_actors(self, movie1_title, movie2_title):
        """Finds actors who appeared in both movies using a SQL JOIN."""
        query = """
        SELECT DISTINCT a.name 
        FROM actors a
        JOIN movie_cast mc1 ON a.id = mc1.actor_id
        JOIN movies m1 ON mc1.movie_id = m1.id
        JOIN movie_cast mc2 ON a.id = mc2.actor_id
        JOIN movies m2 ON mc2.movie_id = m2.id
        WHERE m1.title LIKE ? AND m2.title LIKE ?
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (f"%{movie1_title}%", f"%{movie2_title}%"))
            return [row[0] for row in cursor.fetchall()]