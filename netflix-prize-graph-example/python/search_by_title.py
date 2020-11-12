import sys

from netflix_dal import search_movies_by_title

if len(sys.argv) != 2:
    print('Usage: search_by_title <query>')
    exit(1)

query = sys.argv[1]
result = search_movies_by_title(query)

if len(result) == 0:
    print(f'No movies match “{query}.”')
    exit(0)

for movie in result:
    movie_id = movie.get('movieId')
    print(f"{movie_id if movie_id else movie.id} “{movie.get('title')}” ({movie.get('year')})")
