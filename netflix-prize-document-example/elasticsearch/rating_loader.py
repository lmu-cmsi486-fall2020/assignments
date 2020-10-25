import csv
import re

import requests

"""
This program builds payloads for requests that add ratings to movies.

The index of movies is assumed to be called `movies`.
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

# Elasticsearch index name.
INDEX_NAME = 'movies'


# Helper function for sending movie updates.
def update_ratings(movie_id, ratings):
    response = requests.post(
        f'http://localhost:9200/{INDEX_NAME}/_update/{movie_id}',
        json={ 'doc': { 'ratings': ratings } })

    # Provide some feedback.
    print(f'{movie_id}: {response.status_code}')
    if (response.status_code != 200):
        print(response.json())


current_movie_id = None
current_ratings = []

# Read the files line by line and accumulate them into arrays for the current movie ID.
for ratings_file in RATING_SOURCES:
    with open(ratings_file, 'r+') as f:
        reader = csv.reader(f)
        for row in reader:
            movie_match = MOVIE_LINE.match(row[0])
            if movie_match:
                # We’re done with a movie, so time to POST.
                if current_movie_id is not None:
                    update_ratings(current_movie_id, current_ratings)

                # Set the new movie ID and start a new list of ratings.
                current_movie_id = movie_match.group(1)
                current_ratings = []
            else:
                # Add a rating to the current array.
                viewer_id = int(row[0])
                rating = int(row[1])
                date_rated = row[2]
                current_ratings.append({
                    'viewer_id': viewer_id,
                    'rating': rating,
                    'date_rated': date_rated
                })

# We need to end the very last movie update statement.
update_ratings(current_movie_id, current_ratings)
