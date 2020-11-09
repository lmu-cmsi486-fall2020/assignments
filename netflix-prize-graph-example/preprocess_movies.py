import csv
import sys

"""
This program cleans up the title field of the movie_titles.csv file so that the proper
escapes and delimiters are applied (especially for titles with commas within). This
cleanup is needed for the `neo4j-admin import` function.
"""

# For simplicity, we assume that the program runs where the files are located.
MOVIE_SOURCE = 'movie_titles.csv'
with open(MOVIE_SOURCE, 'r+', encoding='iso-8859-1') as f:
    reader = csv.reader(f)
    writer = csv.writer(sys.stdout)
    for row in reader:
        id = row[0]
        year = None if row[1] == 'NULL' else int(row[1])
        title = ', '.join(row[2:])
        writer.writerow([id, year, title])