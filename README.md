# Movie Database Management System

A Python-based database management system for analyzing movie data from The Movie Database (TMDB) API. This project creates and manages a MySQL database with movie information including genres, actors, budgets, revenues, and popularity metrics.

## Project Team

- **Milana Yakubov** - 213400369
- **Guy Harem** - 312576655

## Features

- **Database Schema**: Creates and manages five interconnected tables (movies, genres, actors, movies_genres, movies_actors)
- **Data Population**: Fetches and stores data for 300+ top-rated English movies from TMDB API
- **Query System**: Five analytical queries to help with movie production decisions
- **Visualization**: Matplotlib integration for displaying popularity trends

## Project Structure

```
.
├── documentation/
│   ├── mysql_and_user_password.txt    # Database credentials
│   └── name_and_id.txt                # Team member information
├── src/
│   ├── api_data_retrieve.py           # TMDB API integration
│   ├── create_db_script.py            # Database schema creation
│   ├── queries_db_script.py           # Query implementations
│   └── queries_execution.py           # Main application interface
├── requirements.txt                    # Python dependencies
└── .gitignore
```

## Requirements

Install required packages using:

```bash
pip install -r requirements.txt
```

### Key Dependencies:
- `mysql-connector-python==9.1.0` - MySQL database connectivity
- `requests==2.32.3` - API data fetching
- `pandas==2.2.3` - Data manipulation
- `matplotlib==3.10.0` - Data visualization
- `prettytable==3.12.0` - Console table formatting

## Database Configuration

Update the database connection parameters in `src/queries_execution.py`:

```python
con = mysql.connector.connect(
    host="localhost",
    port=3305,
    user="your_username",
    database="your_database",
    password="your_password",
)
```

## Database Schema

The database consists of five tables:

1. **movies**: Core movie information (ID, title, release date, popularity, budget, revenue, runtime)
2. **genres**: Genre definitions
3. **actors**: Actor information
4. **movies_genres**: Many-to-many relationship between movies and genres
5. **movies_actors**: Many-to-many relationship between movies and actors (max 5 actors per movie)

Key indexes:
- Budget index on movies table for optimized query performance
- FULLTEXT indexes on title and actor name fields

## Usage

Run the main application:

```bash
python src/queries_execution.py
```

### Available Commands:

- **delete**: Remove all tables from the database (⚠️ Warning: Re-population takes ~2 hours)
- **create**: Create database schema
- **initialize**: Populate database with TMDB data (~2 hours for 300 movies)
- **run**: Execute queries interactively
- **example**: Run pre-configured query examples
- **exit**: Exit the application

## Available Queries

### 1. Genre Profit Analysis (query_1)
Find the top 5 most profitable movies in a selected genre.

**Example**: `execute_query_genre('Action')`

### 2. Actor Popularity (query_2)
Calculate the average popularity of movies featuring a specific actor.

**Example**: `execute_query_actor('Tom Hanks')`

### 3. Title Keyword Revenue (query_3)
Find the average revenue of movies containing a keyword in their title.

**Example**: `execute_query_title('Star')`

### 4. Optimal Runtime (query_4)
Determine the best runtime for a movie given a specific budget (±10% range).

**Example**: `execute_query_runtime(150000000)`

### 5. Release Date Analysis (query_5)
Display average movie popularity for each day of a selected month with visualization.

**Example**: `execute_query_month('January')`

## API Integration

The system uses TMDB API (`src/api_data_retrieve.py`) to fetch:
- Top-rated English movies (300 pages)
- Movie details (budget, revenue, runtime, genres)
- Actor information (top 5 per movie)

## Notes

- Initial data population takes approximately 2 hours for 300 movies
- The database uses `INSERT IGNORE` to prevent duplicate entries
- Foreign key constraints ensure data integrity
- All queries use parameterized statements to prevent SQL injection

## License

This is an academic project for Tel Aviv University Database Management Systems course.