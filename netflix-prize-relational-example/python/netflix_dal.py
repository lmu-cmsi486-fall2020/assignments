import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, func
from sqlalchemy.orm import sessionmaker, relationship

db = create_engine(os.environ['DB_URL'])
metadata = MetaData(db)
movie_table = Table('movie', metadata, autoload=True)
rating_table = Table('rating', metadata, autoload=True)


# Raw SQL-style implementation of a movie query.
def search_movies_by_title(query, limit=100):
    with db.connect() as connection:
        # We want actual %'s so need to escape them in the string.
        result_set = connection.execute(f"""
            SELECT * FROM movie WHERE title ILIKE '%%{query}%%' ORDER BY title LIMIT {limit}
        """)
        result = result_set.fetchall()
        return list(result)


# SQL builder-style implementation of an aggregate query.
def get_average_rating_of_movie(movie_id):
    with db.connect() as connection:
        statement = select([func.avg(rating_table.c.rating)]).where(rating_table.c.movie_id == movie_id)
        result_set = connection.execute(statement)

        # We know in advance that this will be a single row with a single column so we feel safe about hardcoding this.
        # A non-existent movie will yield `None` for this expression.
        return result_set.fetchone()[0]


# For ORM-style implementations, we need to define a few things first.
ORM_Base = declarative_base()


class Movie(ORM_Base):
    __tablename__ = 'movie'
    id = Column(Integer, Sequence('movie_id_seq'), primary_key=True)
    title = Column(String)
    year = Column(Integer)


class Rating(ORM_Base):
    __tablename__ = 'rating'

    # ORM requires some way to guarantee the uniqueness of a row, even if the table itself doesn’t have an official
    # primary key. By marking multiple columns as a “primary_key,” we’re telling ORM that the _combination_ of these
    # values can uniquely identify a row.
    #
    # In our case, we are making the explicit choice that no viewer can rate the same movie more than once.
    # Fortunately, this appears to be true for the given dataset.
    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True) # ForeignKey takes table properties…
    viewer_id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    date_rated = Column(Date)
    movie = relationship('Movie') # …but relationship takes the mapped class


# The notion of a Session is a multifaceted one whose usage and implementation may change depending on the type
# of application that is using this DAL (particularly, a standalone application vs. a web service). It is implemented
# here in the simplest possible way. Note that if this DAL is to be used in other contexts, code surrounding sessions
# may have to change.
#
# At a minimum, we follow the basic SQLAlchemy rule that sessions should be external to the functions that use them.
# Thus, we define current_session at this upper level, and not within each function.
Session = sessionmaker(bind=db)
current_session = Session()


# ORM-style implementation of a rating query.
def get_ratings_by_viewer(viewer_id, limit=100):
    query = current_session.query(Rating).\
        join(Movie).\
        filter(Rating.viewer_id == viewer_id).\
        order_by(Rating.date_rated, Movie.title).\
        limit(limit)

    return query.all()


# ORM-style implementation of a movie inserter.
def insert_movie(title, year):
    movie = Movie(title=title, year=year)
    current_session.add(movie)
    current_session.commit() # Make the change permanent.
    return movie
