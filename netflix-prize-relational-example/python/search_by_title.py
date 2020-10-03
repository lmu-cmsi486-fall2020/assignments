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
    print(f'{movie[0]} “{movie[2]}” ({movie[1]})')
