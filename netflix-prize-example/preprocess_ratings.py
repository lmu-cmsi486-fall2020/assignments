import csv
import re
import sys

# For simplicity, we assume that the program runs where the files are located.
SOURCES = [
    'combined_data_1.txt',
    'combined_data_2.txt',
    'combined_data_3.txt',
    'combined_data_4.txt'
]

DESTINATION = 'ratings.csv'

# The all-important pattern indicating the current movie.
MOVIE_LINE_PATTERN = '^(\d+):$'
MOVIE_LINE = re.compile(MOVIE_LINE_PATTERN)

post_processed_file = open(DESTINATION, 'w')
current_movie_id = None

# Read the files line by line and write them out with the movie ID prepended.
for ratings_file in SOURCES:
    # Provide some visible output so that the user can see where we are.
    print(f'Processing file {ratings_file}...')

    with open(ratings_file, 'r+') as f:
        reader = csv.reader(f)
        for row in reader:
            movie_match = MOVIE_LINE.match(row[0])
            if movie_match:
                # Set the new movie ID.
                current_movie_id = movie_match.group(1)

                # Provide more visible output.
                print(f'- Movie ID: {current_movie_id}')
            else:
                rating_line = ','.join([current_movie_id, *row])
                post_processed_file.write(f'{rating_line}\n')

post_processed_file.close()
