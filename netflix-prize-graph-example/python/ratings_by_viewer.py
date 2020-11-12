import sys
from netflix_dal import get_ratings_by_viewer

if len(sys.argv) != 2:
    print('Usage: ratings_by_viewer <viewer_id>')
    exit(1)

viewer_id = sys.argv[1]
try:
    result = get_ratings_by_viewer(viewer_id)

    if len(result) == 0:
        print(f'The viewer {viewer_id} does not have any ratings in the database.')
        exit(0)

    for record in result:
        rating = record.get('rating')
        movie = record.get('movie')
        date_rated = rating.get('dateRated').iso_format() # neo4j.time.Date object-to-string conversion.
        print(f"{date_rated}: “{movie.get('title')}” got a {rating.get('rating')}.")
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{viewer_id}” is a valid viewer ID.')
