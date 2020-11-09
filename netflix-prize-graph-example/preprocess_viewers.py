import csv
import re

# For simplicity, we assume that the program runs where the files are located.
SOURCES = [
    'combined_data_1.txt',
    'combined_data_2.txt',
    'combined_data_3.txt',
    'combined_data_4.txt'
]

# The all-important pattern indicating the current movie---here we are using it
# just to provide some output guidance.
MOVIE_LINE_PATTERN = '^(\d+):$'
MOVIE_LINE = re.compile(MOVIE_LINE_PATTERN)
current_movie_id = None

DESTINATION = 'viewers.csv'
post_processed_file = open(DESTINATION, 'w')

# Read the files line by line and write out just the viewer IDs.
#
# We compile a list of IDs already seen and filter for uniques here---a choice
# that assumes that we have enough memory to hold all possible IDs. A pre-count
# was done to verify that the number of IDs would indeed fit in memory, so we
# can proceed with this. In the general case, we might not have that luxury.
viewer_ids = {}
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

                # Provide some visible output.
                print(f'- Movie ID: {current_movie_id}')
            else:
                # Write out the viewer ID if we haven’t seen it before.
                viewer_id = row[0]
                if viewer_ids.get(viewer_id) is None:
                    viewer_ids[viewer_id] = True
                    post_processed_file.write(f'{viewer_id}\n')

post_processed_file.close()
