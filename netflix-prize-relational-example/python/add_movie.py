import sys

from netflix_dal import insert_movie

if len(sys.argv) != 3:
    print('Usage: add_movie <title> <year>')
    exit(1)

title = sys.argv[1]
year = sys.argv[2]
try:
    movie = insert_movie(title, int(year))
    print(f'Movie “{movie.title}” ({movie.year}) added with ID {movie.id}.')
except ValueError:
    print(f'Sorry, something went wrong. Please ensure that “{year}” is a valid year.')
