**CMSI 486** Introduction to Database Systems, Fall 2020

# Netflix Prize Graph Database Mini-Stack Example
This folder and README contains sample commands and code that correspond to what is being requested for the [Graph Database Mini-Stack assignment](../README.md). To save repository space, the data files themselves are _not_ included here: before trying out these commands and programs, please [download the files](https://www.kaggle.com/netflix-inc/netflix-prize-data) into this folder first.

To avoid accidental committing of these files, a _.gitignore_ file has been placed here as well. We are definitely not taking an extra two gigabytes of repository space lightly!

## Graph Schemas: A New Node State of Mind
A graph database’s logical schema, with its combination of nodes for entities and edges for relationships, tends to resemble an entity-relationship or UML canonical schema more than other database models, and that is in fact one of its appeals. So we use that as a starting point in writing up our logical schema:

- Identify your _entities_ (nouns)
- State their _attributes_ (adjectives)
- Connect their _relationships_ (verbs)—pay particular attention to directionality because this determines how you read the relationship: `A––likes⟶B` is read “A likes B” (that may seem obvious when reading text but can be trickier in a visual format where arrows may be pointing all over the place)

Importantly, relationships _can also have attributes_—this is something that can make your logical model resemble the real world even more closely than before.

Conversion to a graph data model is then straightforward. In Neo4j notation, it’s virtually identical except for the shapes used:

- Entities become _labeled nodes_ and they are drawn as rounded rectangles, becoming circles when rendered by Node4j
- Attributes of entities become _properties_ which are listed within their respective nodes’ rounded rectangles
- Relationships become _labeled, directed edges_
- Attributes of relationships are listed as _properties_ under their edge labels

For our Netflix Prize data, we leverage the graph data model by, for the first time, preserving the idea of a viewer as an entity. This was overkill in the relational model because we have no information about a viewer outside if their ID; this was prohibitive in the document data model for a similar reason, plus document databases shy away from joins except for very specific use cases. But viewed as a graph, it turns out to be quite natural for viewers to be nodes, even if we only have their IDs:

![Netflix Prize graph schema diagram](./schema-diagram.png)

A version of this diagram with additional annotations is available as [schema.pdf](./schema.pdf).

To help you with your own logical schema, Neo4j provides [a detailed modeling guide](https://neo4j.com/developer/data-modeling/), including [specific suggested conversions when coming from a relational model](https://neo4j.com/developer/relational-to-graph-modeling/). Use these pages to help you make design decisions about your own dataset’s schema as well as for examples on appropriate notation.

## Feed the ’Neo
Similarly to document-centric databases, graph databases do not need a schema up-front: you can start creating nodes and relationships on the spot. Unlike the document-centric databases that we’ve seen and more like relational databases, Neo4j has an actual query language called Cypher which, like SQL, has both DML (data manipulation) and DDL (data definition) capabilities.

In Node4j, instantiating ad hoc nodes and edges involves the Cypher [CREATE](https://neo4j.com/developer/cypher/updating/#_inserting_data_with_cypher) statement. If you create nodes or edges with new labels, that’s equivalent to defining a new type of node or relationship (since the label acts very much like a “type”). Deleting a “type” is pretty much deleting all nodes or edges with a given label, via Cypher’s [DELETE](https://neo4j.com/developer/cypher/updating/#cypher-delete) statement.

## Mass Co-node-sumption
Using [CREATE](https://neo4j.com/developer/cypher/updating/#_inserting_data_with_cypher) is a lot like using `INSERT` in SQL: it adds data one at a time. However, as we’ve seen in other systems, one-at-a-time isn’t the most efficient way to add data. Neo4j has the ability to import nodes and edges from comma-separated value (CSV) files; for smaller files, a [LOAD CSV](https://neo4j.com/docs/cypher-manual/4.1/clauses/load-csv/) statement is available. For something the size of our Netflix Prize data, we want something beefier—and this is available via [_neo4j-admin import_](https://neo4j.com/docs/operations-manual/current/tools/import/) on the command line.

The _neo4j-admin import_ command handles the Netflix Prize data with aplomb, but this capacity comes with a major condition: it can only do this on a _new, unused_ database. Thus, try to get comfortable with putting up or clearing out Neo4j setups first before giving this a shot.

Assuming a level of comfort with setting up and configuring Neo4j (see the [setup guide](http://dondi.lmu.build/share/db/neo4j-setup-day.pdf) for specifics), importing the Netflix Prize data involves the following steps:

1. Set up a fresh “layout” and configuration file for Neo4j
2. Start the server to let it initialize the file structure
3. _Don’t connect or login_—stop the server once startup is complete
4. Run the _neo4j-admin import_ command while the server is stopped

In order for _neo4j-admin import_ to do its work, it needs to be told how to interpret the CSV files that it is given. The key things to extract here are nodes and edges (relationships)—for our case study, that means we have to tell Neo4j how `:Movie` nodes, `:Viewer` nodes, and `:RATED` edges are derived from our dataset.

This interpretation is provided by supplying custom _header files_ which state how each column of each CSV should be interpreted. An example is given [in Neo4j’s Data Import developer guide](https://neo4j.com/developer/guide-import-csv/#batch-importer) and this repository provides headers for the Netflix Prize data. [Full documentation for header files](https://neo4j.com/docs/operations-manual/current/tools/import/file-header-format/#import-tool-header-format) is also available.

### :Movie Nodes
The _movie_titles.csv_ file pretty much corresponds to our planned :Movie nodes, but the file needs one tweak before _neo4j-admin import_ can consume it properly: titles with commas in them need to be delimited properly! The [_preprocess_movies.py_](./preprocess_movies.py) file will do that for us. The file that _it_ produces will be the one that we’ll feed to _neo4j-admin import_:

    python3 preprocess_movies.py > movies.csv

That file’s corresponding [_movie_header.csv_](./movie_header.csv) provides a good introduction to this header format. It consists of a single line (all of these header files do):

    movieId:ID(Movie),year:LONG,title

The header file lists how each comma-separated column is to be named and interpreted. The most distinctive thing here is the `:ID(Movie)` suffix attached to the `movieId` field (the first comma-separated value in the file)—this identifies that column as the identifier (“primary key”) of a :Movie node. The `year` field is given a `LONG` data type to ensure that it is interpreted as such; the `title` is a string by default.

### :Viewer Nodes
Populating :Viewer nodes also comes with a wrinkle, because we don’t have a _viewers.csv_ file per se. Our data includes no other information about a viewer beyond their IDs (appropriately enough, because otherwise they may compromise a viewer’s privacy…well, aside from their viewing habits and tastes 😅), so we must “extract” our viewers from the ratings (_combined_data_) files. The [_preprocess_viewers.py_](./preprocess_viewers.py) program does this by reading viewer IDs from _combined_data_ then writing them out to _viewers.csv_. Duplicates are removed in the process (doable in memory after ascertaining that we can fit the full number of viewer IDs therein):

    python3 preprocess_viewers.py

This program doesn’t write to standard output because it uses that to provide feedback on how far it has gone. It has the _viewers.csv_ filename as part of its code.

With this, it should come as no surprise that the corresponding [_viewer_header.csv_](./viewer_header.csv) file is extremely simple:

    viewerId:ID(Viewer)

That’s all we know about a :Viewer node, with its single `viewerId` property which also serves as its node identifier.

### :RATED Edges
Once the nodes are loaded, we’ll need to connect them. The ratings (_combined_data_) files provide this information, and for compatibility with _neo4j-admin import_ we will recruit an old friend: the [_preprocess_ratings.py_](./preprocess_ratings.py) program from way back in our file assignment (well, maybe not _that_ way back, but it sure feels like it, doesn’t it?). It turns out that this program does exactly what we want for creating :RATED relationship edges—it combs through the _combined_data_ files and creates a new file, _ratings.csv_, with movie IDs prepended to every rating. That way, each line of the new file has the movie that was rated, the viewer who gave the rating, and of course the actual rating value plus date:

    python3 preprocess_ratings.py

Reminder: the resulting _ratings.csv_ file is quite large (2.6 gigabytes for me).

We partner this file with [_rating_header.csv_](./rating_header.csv), which now tells us how to “connect the dots” between viewers and movies via how the viewers rated the movies:

    :END_ID(Movie),:START_ID(Viewer),rating:LONG,dateRated:DATE

Note the two new symbols `:END_ID` and `:START_ID`—this is how we connect the nodes. Our schema, in one sentence, is “Viewer RATED Movie:” thus, the :RATED relationship _starts_ at a viewer and _ends_ at a movie. `:START_ID` and `:END_ID` indicate the _identifiers_ to use in order to match one node to the other.

_neo4j-admin import_ will take those IDs, find them in the database, then _connect_ them with a relationship that has the `rating` and `dateRated` properties. So each line of _ratings.csv_ represents a :RATED edge from a viewer to a movie.

### Enter _node-admin import_
To recap, the full load will require six (6) files: three (3) that you’ll derive from the Netflix Prize data and three (3) that are in this repository:

- _movies.csv_: Created by `python3 preprocess_movies.py > movies.csv`
- _viewers.csv_: Created by `python3 preprocess_viewers.py`
- _ratings.csv_: Created by `python3 preprocess_ratings.py`
- [_movie_header.csv_](./movie_header.csv)
- [_viewer_header.csv_](./viewer_header.csv)
- [_rating_header.csv_](./rating_header.csv)

To put them all together, we invoke the _neo4j-admin import_ command. It will need the same `NEO4J_CONF` environment variable that was given to your Neo4j server installation, so that it knows where to put things. The rest of the command is then about listing the nodes and edges/relationships that it should create:

    NEO4J_CONF=<absolute path to conf directory> neo4j-admin import --nodes=Movie="movie_header.csv,movies.csv" --nodes=Viewer="viewer_header.csv,viewers.csv" --relationships=RATED="rating_header.csv,ratings.csv" --id-type=STRING

The line above is meant for copy-paste-edit into your command line program (once the requisite files are all created). This is how the command breaks down:

| Section | Meaning |
| --- | --- |
| `NEO4J_CONF=<absolute path to conf directory>` | Directory containing _neo4j.conf_ |
| `neo4j-admin import` | The command itself |
| `--nodes=Movie="movie_header.csv,movies.csv"` | Specifies how to load :Movie nodes |
| `--nodes=Viewer="viewer_header.csv,viewers.csv"` | Specifies how to load :Viewer nodes |
| `--relationships=RATED="rating_header.csv,ratings.csv"` | Specifies how to load :RATED edges/relationships |
| `--id-type=STRING` | Indicates that all IDs should be treated as strings |

When you’re ready, unleash _neo4j-admin import_ and let it work. Speed should be on par with _mongoimport_ or our direct Elasticsearch web requests in _rating_loader.py_. You’ll get some progress feedback so you’ll know how far along you are.

Upon completion, fire up _neo4j console_ and point your web browser to http://localhost:7474 to gain access to a humongous graph that connects 480,189 viewers to 17,770 movies in 100,480,507 ways. Make no mistake, this pushes the limits of what Neo4j can handle…and at times surpasses it.

## Can’t Graph This? Cypher Time!
There’s a level of challenge to making an apples-to-apples comparison for the same query between graph databases and other types because part of what makes graph databases different is _the very type_ of query that one can ask. Further, the resource needs of Neo4j, again due to its nature, sometimes far exceeds the computing resources that we may have—another interesting point of comparison but we do want queries that return _something_ so we’ll sometimes need to reduce the scope of what we’re asking so that we don’t ask the system to the point of unresponsiveness.

It’s once more worthwhile to reference the excellent [Getting Started with Cypher](https://neo4j.com/developer/cypher/intro-cypher/) developer guide provided by Neo4j. Probably best to walk through those pages and videos first (trying things out either on a Neo4j Sandbox, Neo4j Desktop, or a local “practice” directory tree of your own) before seeing how Neo4j handles are sizable case study data set.

(waits for you to get through [Getting Started with Cypher](https://neo4j.com/developer/cypher/intro-cypher/))

…

…

…

…

…

### Just the Movies—Single-Node Queries
OK—let’s see how Cypher handles our sample case study queries. The main building blocks for Cypher queries are the [`MATCH`](https://neo4j.com/docs/cypher-manual/4.1/clauses/match/), [`WHERE`](https://neo4j.com/docs/cypher-manual/4.1/clauses/where/), and [`RETURN`](https://neo4j.com/docs/cypher-manual/4.1/clauses/return/) clauses. `MATCH` is somewhat unique because it’s a _pattern matcher_—it lets you specify the subgraph that you are looking for by pseudo-drawing it in ASCII-art-like style. `WHERE` then restricts that subgraph further, in a way that feels a lot like SQL’s `WHERE` clause. Finally, `RETURN` specifies which portions of the matched and filtered pattern should come back as results.

* List all columns for movies containing both `'and'` and `'of'` in their titles, sorted ascending by year then title:
```
MATCH (m:Movie)
WHERE m.title CONTAINS " and " AND m.title CONTAINS " or "
RETURN m
ORDER BY m.year, m.title
```

**Queryer beware:** Right away we run into some unexpected behavior, because although we can certainly formulate and run what appears to be a valid Cypher query above, on my setup I actually get no results. There are definitely movies which meet these two `CONTAINS` predicates—we’ve seen them in the other databases—but for whatever reason, this particular combination returns nothing on my installation of Neo4j. Something comes back for `m.title CONTAINS " and "` by itself and also for `m.title CONTAINS " or "` by itself—and even removing a _space_ or two from those strings produces results—but once we have _exactly_ `m.title CONTAINS " and " AND m.title CONTAINS " or "`, nothing comes back 🤷🏽‍♂️

And yet, _this_ structurally identical query—just with different string matches—returns results:
```
MATCH (m:Movie)
WHERE m.title CONTAINS " Me " AND  m.title CONTAINS " My "
RETURN m
ORDER BY m.year, m.title
```

The text output of this query is:
```
╒══════════════════════════════════════════════════════════════════════╕
│"m"                                                                   │
╞══════════════════════════════════════════════════════════════════════╡
│{"movieId":"11024","title":"For Me and My Gal","year":1942}           │
├──────────────────────────────────────────────────────────────────────┤
│{"movieId":"6379","title":"Life with Judy Garland: Me and My Shadows",│
│"year":2001}                                                          │
└──────────────────────────────────────────────────────────────────────┘
```

The graph output—not hugely useful but a hint of where this can go—looks like this:
![Me and My in the Title](./images/me-and-my-in-title.png)

Note how a graph display effectively ignores the `ORDER BY` clause—“order” in that sense just doesn’t translate to a graph. But it _is_ respected in text or tabular renderings of the query results.

* List movie titles released in the 20th century with the substring `'future'` in their titles, case-insensitively, sorted ascending by title:
```
MATCH (m:Movie)
WHERE toLower(m.title) CONTAINS 'future' AND m.year < 2001
RETURN m.title
ORDER BY m.title
```

The Neo4j version of this query shows how the built-in [`toLower`](https://neo4j.com/docs/cypher-manual/4.1/functions/string/#functions-tolower) function facilitates a case-insensitive string containment predicate—one of [many functions available within Cypher](https://neo4j.com/docs/cypher-manual/4.1/functions/).

Because we only ask for movie _titles_ here, no graph rendering is possible:
```
╒══════════════════════════════════════╕
│"m.title"                             │
╞══════════════════════════════════════╡
│"Back to the Future"                  │
├──────────────────────────────────────┤
│"Back to the Future Part II"          │
├──────────────────────────────────────┤
│"Back to the Future Part III"         │
├──────────────────────────────────────┤
│"Future War"                          │
├──────────────────────────────────────┤
│"Futuresport"                         │
├──────────────────────────────────────┤
│"Ivan Vasilievich: Back to the Future"│
├──────────────────────────────────────┤
│"Megaman: Battle for the Future"      │
├──────────────────────────────────────┤
│"The X-Files: Fight the Future"       │
└──────────────────────────────────────┘
```

However, if we `RETURN m` then we get this (edge-less) graph:
![Future in title before 2001](./images/movies-with-future-before-2001.png)

### Lots of Ratings: Caution
Unlike other systems, the pattern-matching paradigm of Neo4j already inherently works with _groupings_ of data, making aggregation operations appear just like “regular” functions. On the other hand, if the set of matching subgraphs is sufficiently large…beware of performance issues, which might become severe enough to actually thrash the server and cause it to not return anything at all. Our first case study query in this category does make Neo4j cry uncle—we actually have to narrow it down a bit so it returns something.

* Determine the average rating given by all viewers on the month of October, 2004:
```
MATCH (:Viewer)-[r:RATED]->(:Movie)
WHERE date("2004-10-01") <= r.dateRated <= date("2004-10-31")
RETURN avg(r.rating)
```

Technically, the query would be what you see above—but it’s too much for Neo4j (my installation of it, at least). If we narrow it down so that fewer ratings are involved, we do get an answer—here we limit our average to just the October, 2004 ratings of movies _released in 1985_:
```
MATCH (:Viewer)-[r:RATED]->(:Movie { year: 1985 })
WHERE date("2004-10-01") <= r.dateRated <= date("2004-10-31")
RETURN avg(r.rating)
```

This is a single number so no graph rendering is available:
```
╒══════════════════╕
│"avg(r.rating)"   │
╞══════════════════╡
│3.7772946147798825│
└──────────────────┘
```

* List the titles of movies that got a rating of 1 on December 25, 2002, sorted ascending by title:
```
MATCH (:Viewer)-[:RATED { rating: 1, dateRated: date("2002-12-25") }]->(m:Movie)
RETURN m.title
ORDER BY m.title
```

This case study query, when translated to our Neo4j schema, shows how _relationships_ are just as queryable as nodes/entities. For certain application domains, this is a very powerful and intuitive abstraction. Once more we can’t have a graph if we only return a single string propery:
```
╒══════════════════════════════════════════════════════════════════════╕
│"m.title"                                                             │
╞══════════════════════════════════════════════════════════════════════╡
│"102 Dalmatians"                                                      │
├──────────────────────────────────────────────────────────────────────┤
│"13 Conversations About One Thing"                                    │
├──────────────────────────────────────────────────────────────────────┤
│"3000 Miles to Graceland"                                             │
├──────────────────────────────────────────────────────────────────────┤
│"A Couch in New York"                                                 │
├──────────────────────────────────────────────────────────────────────┤
│"A Fish Called Wanda"                                                 │
├──────────────────────────────────────────────────────────────────────┤
  ...
  ...
```

If we instead return _both_ the nodes and relationships that are matched by the query—and limit things a bit so that our results aren’t so humongous—we get this:
```
MATCH (v:Viewer)-[r:RATED { rating: 1, dateRated: date("2002-12-25") }]->(m:Movie { year: 1992 })
RETURN m, r, v
```
![Rated at Christmas 2002, released in 1992](./images/christmas-2002-1992.png)

Looks like viewer `188613` was very much in a ’90s mood on Christmas Day of 2002 (not just ’90s, but **1992** exactly—10-year anniversary of something maybe?). It’s insights like these that graph databases can provide which may be a lot harder to tease out on other data models.

* List the year and rating count for movies released before 1910 or after 2000, sorted descending by year:
```
MATCH (:Viewer)-[r:RATED]->(m:Movie)
WHERE m.year < 1910 OR m.year > 2000
RETURN m.year, count(r)
ORDER BY m.year DESC
```

As you can see, this type of query doesn’t do much to distinguish a graph database from others:
```
╒════════╤══════════╕
│"m.year"│"count(r)"│
╞════════╪══════════╡
│2005    │1983802   │
├────────┼──────────┤
│2004    │10456339  │
├────────┼──────────┤
│2003    │9576604   │
├────────┼──────────┤
│2002    │8640932   │
├────────┼──────────┤
│2001    │7241888   │
├────────┼──────────┤
│1909    │109       │
├────────┼──────────┤
│1896    │152       │
└────────┴──────────┘
```

However, another tweak gives us a more visual look at those 109 + 152 = 261 ratings for movies released before 1910:
```
MATCH (v:Viewer)-[r:RATED]->(m:Movie)
WHERE m.year < 1910
RETURN m, r, v
```
![Released before 1910](./images/ratings-released-before-1910.png)

The possibilities go on and on…the fun never stops!

## Even. Moar. Clauses.
Although `MATCH`, `WHERE`, and `RETURN` (with the occasional `ORDER BY` if you want that non-graph-database feeling) are likely to be your primary Cypher building blocks, they only [scratch the surface](https://neo4j.com/docs/cypher-manual/4.1/clauses/) of the language. Do take a peek to see more of what Cypher can do, ranging from what may feel familiar:

- [`CREATE`](https://neo4j.com/docs/cypher-manual/4.1/clauses/create/)
- [`DELETE`](https://neo4j.com/docs/cypher-manual/4.1/clauses/delete/)
- [`LIMIT`](https://neo4j.com/docs/cypher-manual/4.1/clauses/limit/)
- [`SET`](https://neo4j.com/docs/cypher-manual/4.1/clauses/set/)
- [`SKIP`](https://neo4j.com/docs/cypher-manual/4.1/clauses/skip/)
- [`UNWIND`](https://neo4j.com/docs/cypher-manual/4.1/clauses/unwind/)

…to the more uniquely Neo4j/Cypher/graph-y:

- [`CALL`](https://neo4j.com/docs/cypher-manual/4.1/clauses/call-subquery/)
- [`OPTIONAL MATCH`](https://neo4j.com/docs/cypher-manual/4.1/clauses/optional-match/)
- [`WITH`](https://neo4j.com/docs/cypher-manual/4.1/clauses/with/)
- [`UNION`](https://neo4j.com/docs/cypher-manual/4.1/clauses/union/)

And as a bonus, Neo4j can also [`EXPLAIN` or `PROFILE`](https://neo4j.com/docs/cypher-manual/4.1/query-tuning/#how-do-i-profile-a-query) a query—worth running on these samples or any others to take a peek into how Neo4j gets all those wonderful graphs.

## Node DAL-ium Edge-osa
In the DAL department, examples are provided here in [JavaScript](./nodejs) and [Python 3](./python). Neo4j provides official “drivers” for these languages, as well as [a host of others](https://neo4j.com/developer/language-guides/). As with the other mini-stacks, you’re free to pick any language in your comfort zone that has an official Node4j library.

### Common Characteristics
Neo4j’s official libraries/drivers are semantically very similar across all supported languages. They share the following common elements:
- A unified entry point, typically called `driver`, which takes a database URL and user credentials to provide an entry point to the database (and indeed, this is a common characteristic of pretty much any database library, regardless of type)
- Instantiated `driver`s then provide `session` objects through which Cypher queries can be `run`
- The official libraries follow a just-slightly-modified “pass me a Cypher string” pattern—the `session` object’s `run` function takes a Cypher string within which `$`-prefixed symbols represent variables that can be substituted, thus providing some protection against code-injection attacks
- Substitution mappings are provided depending on a language’s features: in Python, they are appended to the `run` function’s arguments as named parameters; in JavaScript, they are passed as an object after the Cypher string

| Python | JavaScript |
| --- | --- |
| `session.run('MATCH (n:Node {name: $value})', value=<value>)` | `session.run('MATCH (n:Node {name: $value})', { value: <value> })` |

- Query results are provided as a fairly uniform _Result_ object which contains metadata about the query and, most importantly, a _Record_ array which represents the actual return value: each _Record_ includes one entry for every variable/expression returned by the Cypher query, and within each such entry are identifiers, start/end identifiers (for edges), and properties
- As with the `run` function, this common structure is adapted to the specific features of the language—for example, in Python, one accesses records by iterating through the _Result_ object; in JavaScript, `records` is an array property of the _Result_

### Higher-Level Abstractions
You would be right to observe that the official libraries appear to be pretty baseline and low-level—akin to embedded SQL-style libraries with relational databases. Libraries with higher-level abstractions are available (model objects, custom types, etc.) but the only one that is official is the [Java OGM library](https://neo4j.com/developer/neo4j-ogm/) (“OGM” stands for “object-graph mapping”—a play on “object-relational mapping”). You’re free to explore this one if you like; for other languages, Neo4j relies on the developer community for this type of support. Neo4j lists these libraries alongside their official ones.

We have chosen not to use these libraries in the class examples because the intent of the course is to have you walk away with a general, overall perspective on databases. But feel free to go deeper on your own with any of the libraries here if you wish, particularly if you miss that taste of ORM from back in the relational database assignment.

### Configuration Data
Like other database systems, Neo4j’s library primarily needs a database URL to get its work done. For consistency, we retain the `DB_URL` environment variable name in our sample DAL code.

Unlike other database systems though, Neo4j does not support including user credentials in the URL—i.e., you can’t supply a URL like `neo4j://username:password@localhost`. As you’ll see in the DAL samples, the username and password are passed in through a separate `driver` parameter.

Because of this, the sample DALs support two other environment variables: `DB_USER` and `DB_PASSWORD`. For convenience, `DB_USER` only needs to be supplied if the database username isn’t `neo4j`. You _do_ need to supply `DB_PASSWORD` separately however—there is no default password. If you’re uncomfortable with providing your Neo4j password on the command line every time, you can set `DB_PASSWORD` using other environment variable mechanisms, such as through an initialization file or system settings. That’s how production environment variable settings are provided anyway.

Execution specifics are provided in the READMEs of our respective DAL examples.
