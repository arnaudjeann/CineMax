from src.processor import DataProcessor


def main():
    processor = DataProcessor()

    movie_list = [
        ("After Hours", 1985),
        ("Once Upon a Time... in Hollywood", 2019),
        ("Death Proof", 2007),
        ("Se7en", 1995),
        ("La La Land", 2016),
        ("The Substance", 2024)
    ]

    print("--- 📥 Starting Ingestion Phase ---")
    for title, year in movie_list:
        processor.process_file(title, str(year))

    print("\n--- 🔍 Discovery Phase ---")
    shared = processor.db.find_shared_actors("Hollywood", "Se7en")

    if shared:
        print(f"✅ Connection Found! Shared actors: {', '.join(shared)}")
    else:
        print("❌ No direct actor connections found.")


if __name__ == "__main__":
    main()