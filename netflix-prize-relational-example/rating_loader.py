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
RATING_SOURCES = [
    'combined_data_1.txt',
    'combined_data_2.txt',
    'combined_data_3.txt',
    'combined_data_4.txt'
]

# The all-important pattern indicating the current movie.
MOVIE_LINE_PATTERN = '^(\d+):$'
MOVIE_LINE = re.compile(MOVIE_LINE_PATTERN)

current_movie_id = None

# Read the files line by line and write them out as INSERT statements along with the current movie ID.
for ratings_file in RATING_SOURCES:
    with open(ratings_file, 'r+') as f:
        reader = csv.reader(f)
        for row in reader:
            movie_match = MOVIE_LINE.match(row[0])
            if movie_match:
                # Set the new movie ID.
                current_movie_id = movie_match.group(1)
            else:
                # Write out an INSERT statement for the row.
                viewer_id = int(row[0])
                rating = int(row[1])
                rating_date = row[2]
                print(f'INSERT INTO rating VALUES({current_movie_id}, {viewer_id}, {rating}, \'{rating_date}\');')
