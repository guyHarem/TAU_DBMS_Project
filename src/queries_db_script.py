import mysql.connector
import prettytable

#QUERY GENRE#
def query_1(genre, cursor):
    query = "SELECT movies.title, movies.revenue - movies.budget AS profit " \
            "FROM movies, genres, movies_genres " \
            "WHERE genres.name = %s " \
                "AND genres.genre_id = movies_genres.genre_id " \
                "AND movies_genres.movie_id = movies.movie_id " \
            "ORDER BY profit DESC " \
            "LIMIT 5"
    cursor.execute(query, (genre,))
    results_table = prettytable.from_db_cursor(cursor)
    results_table.field_names = ["Title", "Profit"]
    return results_table

#QUERY ACTOR#
def query_2(name, cursor):
    query = """
    SELECT AVG(movies.popularity) AS avg_popularity
    FROM movies
    JOIN movies_actors ON movies.movie_id = movies_actors.movie_id
    JOIN actors ON actors.actor_id = movies_actors.actor_id
    WHERE (
        CASE
            WHEN INSTR(%s, ' ') > 0 THEN actors.name = %s
            ELSE actors.name REGEXP CONCAT('(^|[[:space:]])', %s, '([[:space:]]|$)')
        END
    )
    """
    cursor.execute(query, (name, name, name))
    result = cursor.fetchone()
    
    results_table = prettytable.PrettyTable()
    results_table.field_names = ["Average Popularity"]
    if result and result[0] is not None:
        results_table.add_row([result[0]])
    else:
        results_table.add_row(["No data available"])
    return results_table


#QUERY TITLE#
def query_3(keyword, cursor):
    query = """
    SELECT AVG(movies.revenue - movies.budget) AS avg_revenue
    FROM movies
    WHERE (
        CASE
            WHEN INSTR(%s, ' ') > 0 THEN movies.title = %s
            ELSE movies.title REGEXP CONCAT('(^|[[:space:]])', %s, '([[:space:]]|$)')
        END
    )
    """
    cursor.execute(query, (keyword, keyword, keyword))
    result = cursor.fetchone()
    
    results_table = prettytable.PrettyTable()
    results_table.field_names = ["Average Revenue"]
    if result and result[0] is not None:
        results_table.add_row([result[0]])
    else:
        results_table.add_row(["No data available"])
    return results_table

#QUERY RUNTIME#
def query_4(input_budget, cursor):
    lower_bound = input_budget * 0.9
    upper_bound = input_budget * 1.1
    
    query = """ SELECT AVG(movies.runtime * (movies.revenue / movies.budget)) / NULLIF(AVG(movies.revenue / movies.budget), 0) AS best_runtime
                FROM movies
                WHERE movies.budget BETWEEN %s AND %s
            """
    cursor.execute(query, (lower_bound, upper_bound))
    result = cursor.fetchone()
    results_table = prettytable.PrettyTable()
    results_table.field_names = ["Best Runtime"]
    if result and result[0] is not None:
        results_table.add_row([int(result[0])])  # Convert to integer
    else:
        results_table.add_row(["No data available"])
    return results_table


#QUERY DATE#
def query_5(month, cursor):
    # given a month, for each month date (1-31) find the average popularity of movies released on that day
    query = "SELECT DAY(release_date) AS day, AVG(popularity) " \
            "FROM movies " \
            "WHERE MONTH(release_date) = %s " \
            "GROUP BY DAY(release_date)"
    cursor.execute(query, (month,))
    results_table = prettytable.from_db_cursor(cursor)
    results_table.field_names = ["Day", "Average Popularity"] # for debug
    return results_table