import csv
import json

"""
This program generates direct `mongo` commands from the source Netflix Prize files in order
to set titles and years for a MongoDB database _with movie ratings already loaded_.

The database is assumed to be called `netflix` and the collection of movies is assumed to
be called `movies`.
"""

# For simplicity, we assume that the program runs where the files are located.
MOVIE_SOURCE = 'movie_titles.csv'


# MongoDB database and collection names.
DB_NAME = 'netflix'
COLLECTION_NAME = 'movies'


# We break out our print statement as a helper function.
def print_movie_update(id, year, title):
    set_argument = {
        '$set': {
            'year': year,
            'title': title
        }
    }

    print(f'db.{COLLECTION_NAME}.updateOne(')
    print(f"  {json.dumps({ 'id': id })},")
    print(f"  {json.dumps(set_argument, ensure_ascii=False)}") # ensure_ascii=False forces UTF-8 encoding.
    print(f')')


# Start by making `mongo` use the given database name.
print(f'use {DB_NAME}')


with open(MOVIE_SOURCE, 'r+', encoding='iso-8859-1') as f:
    reader = csv.reader(f)
    for row in reader:
        id = row[0]
        year = None if row[1] == 'NULL' else int(row[1])
        title = ', '.join(row[2:])
        print_movie_update(id, year, title)
