import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document


es = Elasticsearch(hosts=[os.environ['ES_HOST']])
MOVIES_INDEX = 'movies'


def search_movies_by_title(query, limit=100):
    movie_search = Search(using=es, index=MOVIES_INDEX) \
        .query('match', title=query) \
        .sort('title.keyword')[:limit] # `size` is applied via list slicing.

    response = movie_search.execute()
    return response


def get_average_rating_of_movie(movie_id):
    average = Search(using=es, index=MOVIES_INDEX) \
        .query('match', _id=movie_id)

    BUCKET_NAME = 'all_ratings'
    METRIC_NAME = 'average_rating'

    # The `bucket` function nests succeeding aggregations.
    average.aggs \
        .bucket(BUCKET_NAME, 'nested', path='ratings') \
        .metric(METRIC_NAME, 'avg', field='ratings.rating')

    response = average.execute()

    # In this database, it’s possible to have a movie with an empty ratings array.
    # Thus, we return a tuple to differentiate whether we got a movie with that ID.
    return (len(response), response.aggregations[BUCKET_NAME][METRIC_NAME]['value'])


# Helper function for get_ratings_by_viewer.
def rating_from_ratings_by_viewer_hit(hit):
    # Note how this expression is _really_ dependent on the structure returned by the query in
    # `get_ratings_by_viewer`.
    rating = hit.meta.inner_hits['ratings'][0]
    return {
        'date_rated': rating.date_rated,
        'title': hit.title,
        'rating': rating.rating
    }


def get_ratings_by_viewer(viewer_id, limit=100):
    ratings_search = Search(using=es, index=MOVIES_INDEX)

    # This uses the `update_from_dict` technique—useful for cases where you’d rather not navigate
    # the function calls due to the complexity of the query object.
    ratings_search.update_from_dict({
        '_source': {
            'excludes': ['ratings']
        },

        'size': 100,
        'query': {
            'nested': {
                'path': 'ratings',
                'inner_hits': { },
                'query': {
                    'match': { 'ratings.viewer_id': viewer_id }
                }
            }
        },

        'sort': [
            {
                'ratings.date_rated': { # Sorts based on a nested object can be…involved.
                    'order': 'asc',
                    'nested': {
                        'path': 'ratings',
                        'filter': {
                            # And yes, the filter does have to be repeated. See
                            # /reference/current/sort-search-results.html#nested-sorting
                            # in https://www.elastic.co/guide/en/elasticsearch
                            'match': { 'ratings.viewer_id': viewer_id }
                        }
                    }
                }
            },
            'title.keyword'
        ]
    })

    # Here, we demonstrate the approach of restructuring the raw results into something
    # that will be simpler for the caller to use.
    response = ratings_search.execute()
    return [ rating_from_ratings_by_viewer_hit(hit) for hit in response ]


# For the document-centric version of `insert_movie`, we use an ORM-ish feature of the Elasticsearch DSL
# library: the `Document` class. We’re actually underutilizing `Document` here: in a full implementation
# with Elasticsearch DSL, `Document` subclasses can be used to initialize an index from the get-go,
# particularly its mappings. More information on this can be found here:
#
# https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#document-life-cycle
#
class Movie(Document):
    class Index:
        using = es
        name = MOVIES_INDEX


# The original Netflix IDs are an artifact of Netflix’s system; here, ID generation switches
# to how Elasticsearch does it, so IDs of newer movies will _not_ be integers.
def insert_movie(title, year):
    movie = Movie(title=title, year=year)
    movie.save()
    return movie