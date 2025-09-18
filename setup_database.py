#!/usr/bin/env python3

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_favorite_songs_table():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorite_songs (
                song_id INT AUTO_INCREMENT PRIMARY KEY,
                song_title VARCHAR(255) NOT NULL,
                artist VARCHAR(255) NOT NULL,
                album VARCHAR(255),
                genre VARCHAR(100),
                release_year INT,
                rating INT CHECK (rating >= 1 AND rating <= 5),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            ''')
            print("Created favorite_songs table")

            cursor.execute("SELECT COUNT(*) as count FROM favorite_songs")
            result = cursor.fetchone()

            if result['count'] == 0:
                sample_songs = [
                    ('Bohemian Rhapsody', 'Queen', 'A Night at the Opera', 'Rock', 1975, 5, 'A masterpiece of progressive rock'),
                    ('Billie Jean', 'Michael Jackson', 'Thriller', 'Pop', 1982, 5, 'Iconic pop song with amazing beat'),
                    ('Hotel California', 'Eagles', 'Hotel California', 'Rock', 1976, 4, 'Classic rock anthem'),
                    ('Imagine', 'John Lennon', 'Imagine', 'Pop', 1971, 5, 'Beautiful and peaceful message'),
                    ('Sweet Child O\' Mine', 'Guns N\' Roses', 'Appetite for Destruction', 'Hard Rock', 1987, 4, 'Great guitar work')
                ]

                cursor.executemany('''
                INSERT INTO favorite_songs (song_title, artist, album, genre, release_year, rating, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', sample_songs)
                print("Added sample songs")
            else:
                print(f"Table already contains {result['count']} songs")

            connection.commit()
            print("Database setup completed successfully!")

    except Exception as e:
        print(f"Error setting up database: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_favorite_songs_table()