import csv
import re
import sys

"""
This program generates direct SQL statements from the source Netflix Prize files in order
to populate a relational database with those files’ data.

By taking the approach of emitting SQL statements directly, we bypass the need to import
some kind of database library for the loading process, instead passing the statements
directly into a database command line utility such as `psql`.
"""

# For simplicity, we assume that the program runs where the files are located.
MOVIE_SOURCE = 'movie_titles.csv'
with open(MOVIE_SOURCE, 'r+', encoding='iso-8859-1') as f:
    reader = csv.reader(f)
    for row in reader:
        id = row[0]
        year = 'null' if row[1] == 'NULL' else int(row[1])
        title = ', '.join(row[2:])

        # Watch out---titles might have apostrophes!
        title = title.replace("'", "''")
        print(f'INSERT INTO movie VALUES({id}, {year}, \'{title}\');')

# We wrap up by emitting an SQL statement that will update the database’s movie ID
# counter based on the largest one that has been loaded so far.
print('SELECT setval(\'movie_id_seq\', (SELECT MAX(id) from movie));')
