import logging
import mysql.connector
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

tables = {}
tables['movies'] = """
    CREATE TABLE IF NOT EXISTS 
    movies (
        movie_id SMALLINT PRIMARY KEY,
        title VARCHAR(128) NOT NULL,
        release_date DATE,
        popularity DECIMAL(7, 3),
        budget INT,
        revenue INT,
        runtime INT,
        FULLTEXT KEY(title)
    ) ENGINE=InnoDB
    """

tables['genres'] = """
    CREATE TABLE IF NOT EXISTS 
    genres (
        genre_id SMALLINT PRIMARY KEY,
        name VARCHAR(15) NOT NULL
    ) ENGINE=InnoDB
    """

tables['movies_genres'] = """
    CREATE TABLE IF NOT EXISTS
    movies_genres (
        movie_id SMALLINT,
        genre_id SMALLINT,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    ) ENGINE=InnoDB
    """

tables['actors'] = """
    CREATE TABLE IF NOT EXISTS
    actors (
        actor_id SMALLINT PRIMARY KEY,
        name VARCHAR(45) NOT NULL,
        FULLTEXT KEY(name)
    ) ENGINE=InnoDB
    """

tables['movies_actors'] = """
    CREATE TABLE IF NOT EXISTS
    movies_actors (
        movie_id SMALLINT,
        actor_id SMALLINT,
        PRIMARY KEY (movie_id, actor_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
    ) ENGINE=InnoDB
    """

# Create tables
def create_tables(cursor):
    for table_name, table_creation_stmt in tables.items():
        logging.info(f"Creating table {table_name}")
        try:
            cursor.execute(table_creation_stmt)
        except mysql.connector.Error as err:
            logging.error(f"Error creating table {table_name}: {err}")
            raise Exception(str(err))
        
        # Create index on budget column in movies table
    logging.info("Creating index on budget column in movies table")
    try:
        cursor.execute("CREATE INDEX idx_budget ON movies(budget);")
    except mysql.connector.Error as err:
        logging.error(f"Error creating index on budget column: {err}")
        raise Exception(str(err))

# Delete tables
def delete_tables(cursor):
    logging.info("Disabling foreign key checks")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table_name in tables.keys():
        logging.info(f"Deleting table {table_name}")
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        except mysql.connector.Error as err:
            logging.error(f"Error deleting table {table_name}: {err}")
            raise Exception(str(err))
    logging.info("Enabling foreign key checks")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
