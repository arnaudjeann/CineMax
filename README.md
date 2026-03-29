# CineMax 🎬

A high-performance Python tool designed to map and explore relationships between movies using the TMDB API and a relational SQLite architecture.

## 🚀 Key Features
- **Automated Ingestion**: Fetches rich metadata (Director, Top Cast, Overview) directly from TMDB.
- **Relational Mapping**: Implements a Many-to-Many database schema to link actors across different productions.
- **Connection Discovery**: Specialized SQL logic to identify shared cast members between any two films in the database.
- **Environment Security**: Secure API key management using `.env` files.

## 🛠 Tech Stack
- **Language**: Python 3.12
- **Database**: SQLite3 (Relational)
- **APIs**: The Movie Database (TMDB) v4 Auth
- **Libraries**: `requests`, `python-dotenv`

## 📂 Architecture
The project follows a modular software engineering approach:
- `src/api_client.py`: Handles asynchronous-ready HTTP requests to external services.
- `src/database.py`: Manages the SQL schema, data integrity, and complex joins.
- `src/processor.py`: The business logic layer that coordinates data flow.

## ⚙️ Installation & Setup
1. Clone the repository.
2. Install dependencies: `pip install requests python-dotenv`
3. Create a `.env` file at the root and add your token:
   ```text
   TMDB_API_KEY=your_v4_token_here