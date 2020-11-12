import os

from neo4j import GraphDatabase


# This is for convenience since the `neo4j` user is known to be created by default.
# We do still let an environment variable override it if needed.
db_user = os.environ['DB_USER'] if os.environ.get('DB_USER') else 'neo4j'


# The Neo4j documentation calls this object `driver` but the name `db` is used here
# to provide an analogy across various DAL examples.
db = GraphDatabase.driver(os.environ['DB_URL'], auth=(db_user, os.environ['DB_PASSWORD']))


def search_movies_by_title(title_query, limit=100):
    with db.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)
            WHERE toLower(m.title) CONTAINS toLower($title_query)
            RETURN m
            ORDER BY m.title
            LIMIT $limit
            """,
            title_query=title_query, # The `query` parameter name is already taken.
            limit=limit)

        # The result needs to be consumed while the session is open.
        return [record.get('m') for record in result]


def get_average_rating_of_movie(movie_id):
    with db.session() as session:
        result = session.run(
            """
            MATCH (m:Movie)<-[r:RATED]-(:Viewer)
            WHERE (exists(m.movieId) AND m.movieId = $movie_id) OR
                  (NOT exists(m.movieId) AND id(m) = $identity)
            RETURN avg(r.rating)
            """,
            movie_id=str(movie_id), # movie_id is passed as an int so we need to convert to a string here.
            identity=movie_id)

        # We know in advance that this will be a single record so we feel safe about hardcoding this.
        # A non-existent movie will yield `None` for this expression.
        return result.single().get('avg(r.rating)')


def get_ratings_by_viewer(viewer_id, limit=100):
    with db.session() as session:
        result = session.run(
            """
            MATCH (viewer:Viewer {viewerId: $viewer_id})-[rating:RATED]->(movie:Movie)
            RETURN viewer, rating, movie
            ORDER BY rating.dateRated, movie.title
            LIMIT $limit
            """,
            viewer_id=viewer_id,
            limit=limit)

        # The result needs to be consumed while the session is open.
        return [record for record in result]


def insert_movie(title, year):
    with db.session() as session:
        result = session.run(
            """
            CREATE (insertedMovie:Movie {title: $title, year: $year})
            RETURN insertedMovie
            """,
            title=title,
            year=year)

        # This returns the full node so we have its identity and labels.
        return result.single().get('insertedMovie')
