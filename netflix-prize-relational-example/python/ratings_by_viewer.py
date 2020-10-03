import sys
from netflix_dal import get_ratings_by_viewer

if len(sys.argv) != 2:
    print('Usage: ratings_by_viewer <viewer_id>')
    exit(1)

viewer_id = sys.argv[1]
try:
    result = get_ratings_by_viewer(int(viewer_id))

    if len(result) == 0:
        print(f'The viewer {viewer_id} does not have any ratings in the database.')
        exit(0)

    for rating in result:
        print(f'{rating.date_rated}: “{rating.movie.title}” got a {rating.rating}.')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{viewer_id}” is a valid viewer ID.')
