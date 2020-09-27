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

# The all-important pattern indicating the current movie.
MOVIE_LINE_PATTERN = '^(\d+):$'
MOVIE_LINE = re.compile(MOVIE_LINE_PATTERN)

# Check for arguments.
if len(sys.argv) != 2:
    print('Usage: query_ratings.py <movie_id>')
    exit()

query_movie_id = sys.argv[1]
movie_found = False

# Read the files line by line until we locate the movie being requested.
for ratings_file in SOURCES:
    with open(ratings_file, 'r+') as f:
        reader = csv.reader(f)
        for row in reader:
            movie_match = MOVIE_LINE.match(row[0])
            if movie_match:
                # Check if we have found the movie we're looking for.
                current_movie_id = movie_match.group(1)
                if current_movie_id == query_movie_id:
                    movie_found = True
                else:
                    # If we have already found the movie and we have changed
                    # movies, then we are done because ratings are grouped
                    # together by movie---once we have found the ratings for
                    # a given movie, we know that we have found them all.
                    if movie_found:
                        exit()
            elif movie_found:
                # We can get fancier about how we print the result but that
                # isn't necessary for our purposes.
                print(row)
