import sys

from netflix_dal import get_average_rating_of_movie

if len(sys.argv) != 2:
    print('Usage: average_rating <movie_id>')
    exit(1)

movie_id = sys.argv[1]
try:
    movie_count, result = get_average_rating_of_movie(movie_id)

    if movie_count == 0:
        print(f'There is no movie with ID {movie_id}.')
        exit(0)

    if result is None:
        print(f'The movie with ID {movie_id} has no ratings yet.')
        exit(0)

    print(f'The average rating of movie ID {movie_id} is {result}.')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{movie_id}” is a valid movie ID.')