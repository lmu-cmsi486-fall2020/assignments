**CMSI 486** Introduction to Database Systems, Fall 2020

# Netflix Prize File Database Mini-Stack Example
This folder and README contains sample commands and code that correspond to what is being requested for the [File Database Mini-Stack assignment](../README.md). To save repository space, the data files themselves are _not_ included here: before trying out these commands and programs, please [download the files](https://www.kaggle.com/netflix-inc/netflix-prize-data) into this folder first.

To avoid accidental committing of these files, a _.gitignore_ file has been placed here as well. We are definitely not taking an extra two gigabytes of repository space lightly! (potentially nearly double that, if you run the pre-processing example as well)

## Pure Command Queries
The following commands are meant to be copy-pasted directly into the command line, with values edited as needed. The command environment used must have `grep`, `awk`, and `wc` available in its path.

### Find Movies Whose Title Matches a Regular Expression
The structure of _movie_titles.csv_ makes it relatively straightforward to use `grep` in order to search for movies by regular expression match (with some caveats). Angle brackets `<>` indicate the portion of the command that you can customize to specify a different match condition:

    grep "<regex>" movie_titles.csv

For example, this will list all movies with “Home” in their titles:

    grep "Home" movie_titles.csv

This will list all movies whose titles end with “Forever”—which works solely because the movie titles are at the _end_ of file’s lines:

    grep "Forever$" movie_titles.csv

The “beginning” directive `^` cannot be used for matching movies whose titles _begin_ with a certain expression because `^` refers to the beginning of a line. This forces us to take into account that each movie title line starts with two comma-separated numbers. So movies whose titles start with _regex_ would need to be found in this way:

    grep "^\d*,\d*,You " movie_titles.csv

…which will give us all movies whose titles begin with the word “You.”

Note that we are now relying on the assumption that the _movie_titles.csv_ file is formatted in a consistent way, including that all IDs and years are numeric and non-blank.

Speaking of which, _are_ there movies with no ID? Are there movies with no year? It would be nice to know for sure, wouldn’t it?

#### Processing the Commas with `awk`
If the `\d*,\d*,` approach feels hacky to you, one might be able to turn to something like `awk` which can be told to separate on commas. This feels a little more fluent—assuming you’ve learned enough `awk` to get to this point:

    awk -F, '$3 ~ /^You / { print }' movie_titles.csv

…the `-F,` argument tells `awk` to separate the fields out by commas, thus making `$1` represent the movie ID, `$2` the release year, and `$3` the movie title…mostly 😅 (can you think of why there is a “mostly” qualifier to that?)

#### Find _How Many_ Movies Match a Regular Expression
With _movie_titles.csv_ being line-based, _counting_ results becomes a matter of sending the `grep` or `awk` output to `wc` by the handy-dandy pipe directive (`|`). Appending `| wc` to any of the commands above will tell you how many movies (lines) matched the preceding filter.

    grep "^\d*,\d*,You " movie_titles.csv | wc
    awk -F, '$3 ~ /^You / { print }' movie_titles.csv | wc

### Find Movies Released in a Certain Year (or Years)
Given the preceding information, performing “queries” using the release year should follow relatively well, with the continuing awkwardness of having to factor in those commas in `grep`. Looks a little easier to read with `awk` though:

    grep "^\d*,<year>," movie_titles.csv
    awk -F, '$2 == <year> { print }' movie_titles.csv

With the express condition in `awk`, you have a little more power—comparators!

    awk -F, '$2 > <year> { print }' movie_titles.csv
    awk -F, '$2 < <year> { print }' movie_titles.csv

Although yes, you can list specific years with `grep`:

    grep -E "^\d*,(1990|1995|2000)," movie_titles.csv

(you’ll need the `-E` or “extended” argument in order to use the `|` syntax)

### Find All Ratings Given by a User
The _movie_titles.csv_ file contains 17,770 movies (one line per movie, 17,770 lines total in the file)—this would be considered small. The _combined_data_ files, however, contain over 100,000,000 individual ratings—to paraphrase something the late great Dr. Phil Dorin used to say, “now we’re talkin’ _real_ data.” Despite some issues with their structure (as seen in the next section), there are _some_ things that we can still do with `grep` and `awk` on these files.

This command, for example, will list all the ratings that a particular user has ever given:

    grep -E "^<user ID>," combined_data_*.txt
    awk -F, '$1 == "<user ID>" { print }' combined_data_*.txt

Note how `grep` can be told to scan multiple files, and it will recognize that by prepending each output line with the file from which it found the line.

`awk`’s comparators can get a little more sophisticated, capable, say, of extracting all of the ratings given by a user that are below 3:

    awk -F, '$1 == "<user ID>" && $2 < 3 { print }' combined_data_*.txt

In both of these examples, you’ll notice one omission that would otherwise be quite useful: the _movies_ that these ratings pertain to. Without that, all we get is a general feel for how a particular viewer rates movies, without knowing what those movies are. Thus, even if we can do _some_ things with `grep` and `awk` on the _combined_data_ files, they still fall short now that the lines of the file no longer have all of the available information on a given rating.

## Program that Reads the Files to Perform a Query

### When to Balk at `grep` and `awk`
Direct commands can work with _movie_titles.csv_ because that file is in a form which aligns with utilities like `grep` and `awk`—namely, the files are line-based, with one line containing complete information for what we would perceive as one “record” in the database (in this case, a movie).

The tools fall short, however, with the _combined_data_ files (which contain the ratings) because those files do _not_ contain complete information per line. Instead, they look like this:

```text
1:
1488844,3,2005-09-06
822109,5,2005-05-13
885013,4,2005-10-19
30878,4,2005-12-26
823519,3,2004-05-03
893988,3,2005-11-17
# …etc.…
4500:
2532865,4,2005-07-26
573364,3,2005-06-20
1696725,3,2004-02-27
1253431,3,2004-03-31
1265574,2,2003-09-01
1049643,1,2003-11-15
1601348,4,2005-04-05
1495289,5,2005-07-09
1254903,3,2003-09-02
2604070,3,2005-05-15
# …etc.…
9211:
1277134,1,2003-12-02
2435457,2,2005-06-01
2338545,3,2001-02-17
2218269,1,2002-12-27
441153,4,2002-10-11
1921624,2,2005-08-31
2096652,3,2004-05-31
818736,2,2004-02-17
284560,3,2003-07-27
1211224,5,2004-05-08
# …you get the idea…
```

Specifically, these files _do not include the movie ID on every line_. Instead, the movie ID is specified with a line that has just the movie ID followed by a colon (`:`). The assumption then is that all lines after that are reviews _for that movie_ until you then hit the next `<number>:` line.

This structure compels us to just write _our own_ programs to find the desired information from these files.

_Small disclaimer:_ Given the legendary status of `awk`, it wouldn’t shock me if there actually _were_ a way to make `awk` differentiate the `<movie ID>:` lines from the rest, then selectively only print the ratings lines immediately after the desired movie ID. I just wouldn’t be the one to tell you how 😬

### Querying for All Ratings of a Particular Movie
One such program can be seen with [query_ratings.py](./query_ratings.py). The program, overall, is straightforward: given a movie ID, it scans the _combined_data_ files until it finds the line indicating the start of the ratings for that movie, `<movie ID>:`. Having found that line, the program then just echoes every rating line until it gets to the next movie, at which point it quits:

    python3 query_ratings.py <movie ID>

This is all well and good, but trying this program out a few times, especially for movies that don’t show up until _combined_data_4.txt_, will quickly (or not) reveal its shortcomings. There must be a better way, right?

### Computing the Average Rating of a Particular Movie
But before we move on thinking that writing our own program was an act of futility, take note of [average_ratings.py](./average_ratings.py). With the full flexibility of a programming language at our finger tips, note how it doesn’t take that much of a leap to now write a program that will give us the average rating of a given movie ID:

    python3 average_ratings.py <movie ID>

The structure of the program is largely the same as that of [query_ratings.py](./query_ratings.py), except that, while scanning the lines that contain a movie’s ratings, we add up the rating scores and calculate their average at the end.

How about finding the movie with the highest average rating? Ehrm we shall “leave that as an exercise” 😅

## Preprocessing Program and Queries that Use Its Output
After seeing the `grep` and `awk` examples followed by the issues encountered when a data file does _not_ fit the mold of what `grep` and `awk` can use, one might then think—what if we generate files that _do_ work well with `grep` and `awk`? In our case, we just need to “unroll” those `<movie ID>:` lines so that the movie ID _does_ get included with every line. If we do this, then the task of finding all ratings for a particular movie may now be doable via `grep` or `awk`.

A program that does just this is given with [preprocess_ratings.py](./preprocess_ratings.py). This program follows the same structure as [query_ratings.py](./query_ratings.py), but instead of merely repeating the ratings lines of that file (then stopping upon reaching the requested movie ID), the preprocessing flavor reads _all_ of the _combined_data_ files and writes every line into a new file, _ratings.txt_, with the movie ID _prepended to every line_.

After running this preprocessor (do try it, but give it some time to finish!—the program sends some progress output so that you know how far along it is), `grep` and `awk` can now be used on _ratings.txt_ in order to find all of the ratings for a given movie:

    grep "^<movie ID>," ratings.txt
    awk -F, '$1 == <movie ID> { print }' ratings.csv

One difference in behavior between [query_ratings.py](./query_ratings.py) and its `grep` and `awk` equivalents (upon creation of _ratings.txt_) is that [query_ratings.py](./query_ratings.py) “knows” to stop once it has found the intended movie’s ratings because it makes an assumption (which is fortunately true) that the _combined_data_ files clusters all of the ratings for a given movie together. There is no way to convey that assumption to `grep` and `awk` (short of hitting <kbd>Control</kbd>-<kbd>C</kbd> once you see the results)—those programs don’t stop on their own until they have read the entire file.

On the one hand, this means that those files can mix up ratings up all over—ratings for the same movie don’t have to be all together. On the other hand, well…they always have to read the entire file. Which tradeoff would you prefer?

## Command/Program Combinations for “Traversing” Relationships in the Data
Note how, even with preprocessing, we’ve been using just movie IDs when querying or returning ratings results. The idea of then “joining” that information with the right line in _movie_titles.csv_ becomes a whole other matter.

For now, we’ll just issue additional commands to find the additional movie information from _movie_titles.csv_. Thus, if we check for all the ratings given by a particular user in our processed _ratings.csv_ file:

    grep -E "^\d*,<user ID>," ratings.csv
    awk -F, '$2 == "<user ID>" { print $1, $3 }' ratings.csv

…we can then pass along the movie IDs to additional `grep`s or `awk`s:

    grep "^<movie ID n>," movie_titles.csv
    awk -F, '$1 == "<movie ID n>" { print }' movie_titles.csv

Yes there is a degree of manual-ness to it, but at least there’s a structure to it that hints at how one might be able to include this in a program.

## Takeaways
So that’s a taste of what it would take to navigate large datasets purely at the level of the raw files in which they are delivered. In a conclusion that should surprise no one, after doing this, you are probably quite ready for a better way to do things. Nevertheless, the exercise is useful for a number of reasons:
- Data distributed in raw files of varying formats will never quite go away—sometimes it’s the only way to pass data around. Thus, it remains useful to have some skills handy for working with these files and exploring them.
- Generalized database management systems, under the hood, _still do store data in files_. Thus, I hope that this exercise sparks your brain somewhat in terms of exactly _what_ goes into “real database” files which facilitates great flexibility, performance, and power. They’re still files after all. Clearly there is an organizational approach to such files that permits better performance and traversal. The effectiveness of that approach is a strong factor in determining the success of a particular database management system.
