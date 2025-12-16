import logging
import requests
import mysql.connector
from mysql.connector import errorcode

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1MGNlZjgzYzY3NzY5MDRjMjYxMTcxODgzMTcyZTE4YiIsIm5iZiI6MTczNjg4NDY5OC41MTUsInN1YiI6IjY3ODZjMWRhZGI0ZmUwMjJhZDRlYTBiNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.j1c8TKT4c9CDSgu8n9d8ay5L6_8wxxhJkB4jSCas_Iw"
BASE_URL = "https://api.themoviedb.org/3"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

SQL_INSERT_GENRE = """
INSERT IGNORE INTO genres (genre_id, name)
VALUES (%s, %s)
"""

SQL_INSERT_MOVIE = """
INSERT IGNORE INTO movies (movie_id, title, release_date, popularity, budget, revenue, runtime)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

SQL_INSERT_MOVIE_GENRE = """
INSERT IGNORE INTO movies_genres (movie_id, genre_id)
VALUES (%s, %s)
"""

SQL_INSERT_ACTOR = """
INSERT IGNORE INTO actors (actor_id, name)
VALUES (%s, %s)
"""

SQL_INSERT_MOVIE_ACTOR = """
INSERT IGNORE INTO movies_actors (movie_id, actor_id)
VALUES (%s, %s)
"""

def fetch_data(partial_url, name, pages, field_filter=None, field_value=None):
    results = []
    curr_url = f"{BASE_URL}{partial_url}"
    for page in range(1, pages + 1):
        logging.info(f"Fetching data from page {page}")
        try:
            response = requests.get(f"{curr_url}&page={page}", headers=headers)
            response.raise_for_status()
            result = response.json().get(name, [])
            if len(result) != 0:
                if field_filter is not None and field_value is not None:
                    if result[0][field_filter] == field_value:
                        results.extend(result)
                else: # no filter
                    results.extend(result)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data: {e}")
            return None
    logging.info(f"Successfully fetched {len(results)} items")
    return results

def fetch_movie_data(movie):
    try:
        logging.info(f"Fetching movie: {movie['title']}")
        curr_url = f"{BASE_URL}/movie/{movie['id']}?language=en-US"
        response = requests.get(curr_url, headers=headers)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

def insert_data(cursor, con):
    movies = fetch_data("/movie/top_rated?language=en-US", "results",300, 'original_language', 'en')

    for movie_general in movies:
        actors_num = 0
        movie = fetch_movie_data(movie_general)
        logging.info(f"Processing movie: {movie.get('id', 'unknown')} - {movie.get('title', 'unknown')}")
        try:
            logging.info(f"Inserting movie: {movie['id']}")
            cursor.execute(SQL_INSERT_MOVIE, (
                movie['id'], movie['title'], movie['release_date'], movie['popularity'],
                movie['budget'], movie['revenue'], movie['runtime']
            ))
            con.commit()
            # Fetch and insert actors, max 5 for each movie#
            actors = fetch_data(f"/movie/{movie['id']}/credits?language=en-US", "cast", 1)
            for actor in actors:
                if actors_num < 5:
                    logging.info(f"Inserting actor: {actor['id']} - {actor['name']}")
                    try:
                        cursor.execute(SQL_INSERT_ACTOR, (actor['id'], actor['name']))
                        con.commit()
                        cursor.execute(SQL_INSERT_MOVIE_ACTOR, (movie['id'], actor['id']))
                        con.commit()
                        actors_num += 1
                    except mysql.connector.Error as err:
                        logging.error(err)
            # Fetch and insert genres
            genres = movie.get('genres', [])
            for genre in genres:
                genre_name = genre['name']
                genre_id = genre['id']
                logging.info(f"Inserting genre: {genre_id} - {genre_name}")
                try:
                    cursor.execute(SQL_INSERT_GENRE, (genre_id, genre_name))
                    con.commit()
                    cursor.execute(SQL_INSERT_MOVIE_GENRE, (movie['id'], genre_id))
                    con.commit()
                except mysql.connector.Error as err:
                    logging.error(err)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                logging.warning(f"Duplicate entry for movie: {movie['id']}")
                continue
            else:
                logging.error(err)
