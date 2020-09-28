**CMSI 486** Introduction to Database Systems, Fall 2020

# Assignment 1019
Alright, we’re in hardcore database mode now—this is the first of three assignments whose goal is to give you firsthand, hands-on (“firsthands-on?”) experience with a particular implementation of a particular database modeling (logical schema) approach. To start, we explore the relational database model, as implemented by [PostgreSQL](https://www.postgresql.org).

Because the upcoming three assignments are essentially variations on the same theme, they are structured similarly:
* For continuity, the remaining assignments for the semester will have the same groups/teams, chosen by you rather than at random
* From this point on, you will base your work on the same dataset—this way, you can have an apples-to-apples perspective on how different database systems handle the same canonical schema
* Along these lines, each database modeling approach will also get its own treatment of our on-going Netflix Prize case study
* Using the same dataset will also allow for more straightfoward performance and efficiency comparisons

With that in mind, let’s move on to our first stop…the relational database model.

## Background Reading
Now is the time to commit to and really get to know a specific dataset, so take one finalizing look at the [Kaggle](https://www.kaggle.com/datasets) and [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets) collections in order to give a rose to 🌹 or put a ring on 💍 “the one” that you’ll be using for the rest of the semester. As before the [Netflix Prize](https://www.kaggle.com/netflix-inc/netflix-prize-data) dataset is used as the case study for the assignment’s accompanying examples—you may not use it for your own submission, but by all means download these files and try out [the given examples](./netflix-prize-relational-example) for yourself.

### Theoretical/Conceptual Reading
The relational database model has a great deal of conceptual and theoretical coverage in the literature, at both formal/academic and practical/tutorial levels. As a fan of primary sources, I highly recommend that you must at least take a peek at the work that started it all: E. F. Codd’s über-seminal work [“A relational model of data for large shared data banks.”](https://dl.acm.org/doi/10.1145/362384.362685) Clocking in at just ten 2-column pages, it still pretty much captures the essence of the database model that continues to have wide adoption and utility nearly half a century later. Definitely not to be missed.

In the Elmasri & Navathe textbook, in-depth coverage of the relational model can be found in Chapters 5-9, “The Relational Data Model and SQL,” with Chapter 8 focusing on the theory and mathematics of the relational data model and Chapter 9 examining common practices in translating a canonical schema into the relational approach. Chapters 10-11 “Database Programming Techniques” discuss how computer programs interact with a relational database, although specific technologies move much faster than the book so these chapters are best used for context and background rather than specific code examples. The book switches back to theory in Chapters 14-15, “Database Design Theory and Normalization.”

Ullman’s [Foundations of Computer Science Chapter 8](http://infolab.stanford.edu/~ullman/focs/ch08.pdf) is now applicable to the assignment in nearly its entirety, with a slight de-emphasis on the sections regarding implementation—we had more of a taste of that in the prior assignment on working directly with files.

### Technical/Operational Reading
Direct technical assistance for the action items in this assignment can be found primarily in the [PostgreSQL documentation site](https://www.postgresql.org/docs/current/index.html). References/tutorials in SQL in general may also help, but always keep an eye out for parts that may have dialect-specific variants in PostgreSQL.

The [_psql_ section](https://www.postgresql.org/docs/current/app-psql.html) of the official PostgreSQL documentation is pretty much everything you can possibly know about this baseline utility for interacting with a PostgreSQL database. If a feature isn’t described there, then it’s probably something that _psql_ can’t do.

Your language of choice will determine the additional readings. The earlier links for working with files will still apply when implementing the “loader” portion of the assignment. New to the pool of documentation are assorted links to relational database libraries across various languages:
* [SQLAlchemy](https://www.sqlalchemy.org) is likely your best bet if you want to interact with PostgreSQL (and other relational database management systems) in Python
* [Sequelize](https://sequelize.org/master) is the corresponding library if Node.js is your jam
* For Java, [JDBC](https://docs.oracle.com/javase/tutorial/jdbc/basics/index.html) (Java Database Connectivity) is actually a first-party feature of the language, though ironically the primary-source documentation linked here is actually getting quite long in the tooth (they say so themselves) so you may well find better and more updated sources out there

## For Submission: Relational Database Mini-Stack
For this assignment, you are asked to build the beginnings of a _relational database_ persistence layer for an envisioned application that is based on your chosen dataset. A working example of such a persistence layer is provided for our on-going Netflix Prize case study.

### SQLFlix: _netflix-pratice.md_, Relational Database Edition
Limber up with the [Netflix Prize relational database mini-stack case study](./netflix-prize-relational-example): study the logical schema; study and run the given loader programs so that you have the dataset in relational form (giving the ratings loader, in particular, ample time to finish!); study and run the sample programs to see how they and their respective libraries interact with PostgreSQL.

With that background in mind, implement the queries listed below, providing the following items for each in _netflix-practice.md_:
* State the criteria in English
* Provide the SQL query that yields those results
* Include a screenshot of this SQL query being issued in _psql_ alongside the first few results

**Precision is the thing:** Make sure that your SQL statements provide _exactly_ the information requested. For example, if the request is for “the number of reviews” that meet a certain condition, don’t provide a query that lists the reviews and requires the user to look at how many reviews were returned; _the query itself_ must provide the number directly. Similarly, for queries that ask for the “highest” or “lowest” values of something, don’t provide a query that lists multiple results, expecting the user to look for the desired result on their own—again, the query must return _precisely_ the row or rows that contain the requested values.

1. _Movies filtered by title and/or year_: A query that retrieves the _ID_, _year_, and _title_ of movies that fit criteria of your choosing (e.g., movies with certain titles or title patterns, movies released on one or more given years, etc.), sorted ascending by _title_
2. _Number of movies released per year_: A query that takes movie criteria of your choosing and returns a table consisting of _year_ and _count_ where _count_ is the number of movies that meet these criteria which were released on that _year_, sorted ascending by _year_
3. _Years with the most movies released_: A query that takes movie criteria of your choosing and returns the same table as above except it only returns the _year_ and _count_ of the _top five (5) years_ with the most movies released, sorted descending by _count_ then ascending by _year_ in case of a tie
4. _Movies rated a certain way by a specific user_: A query that lists the _title_ and _year_ of movies seen by a particular user with a rating matching conditions of your choosing (e.g., 4 and above, 2 and below, etc.) sorted ascending by _title_
5. _Average rating of movies_: A query that takes movie criteria of your choosing and returns a table consisting of _title_, _year_, and _avg_ where _avg_ is the average rating received by each movie, sorted descending by _avg_ (thus listing the top-rated movie first) then ascending by _title_ in case of a tie
6. _Specific average rating of movies_: A query that takes movie criteria of your choosing and returns a table consisting of _title_, _year_, and _avg_ where _avg_ is the average rating received by each movie _and_ meeting some condition of your choosing such as average greater than 4, average less than 3, etc.—the results should be sorted descending by _avg_ (thus listing the top-rated movie first) then ascending by _title_ in case of a tie
7. _Number of reviews received by a movie during a certain time period_: A query that takes movie criteria of your choosing and returns a table consisting of _title_, _year_, and _count_ where _count_ is the number of reviews received by each movie _within a particular date range_ of your choosing such as after 2005, during the month of September, etc.—the results should be sorted descending by _count_ (thus listing the most-frequently-rated movie first) then ascending by _title_ in case of a tie

For each of these queries, find ways to “sanity-check” your work—are there ways to run other queries that will help you verify whether you are really getting the results you’ve requested? It’s useful to do this at first while you’re still getting the hang of SQL.

### Game, Dataset, & Match: _about.md_, _.gitignore_
This assignment marks a moment of “commitment:” you will settle into groups that should last through the end of the semester, and your new long-term group is also expected to settle on a dataset that will stay with you as well. After making this final selection, for one last time (except for a little redux in the full database stack) describe your chosen dataset in an _about.md_ Markdown file. State the following:
* What the dataset contains
* What applications would find the dataset useful
* What kinds of questions might such applications ask of this dataset

As with prior assignments, make sure that _about.md_ also has links to the actual dataset, for anyone who would like to download a copy for themselves. Also as before, whatever you do, do _not_ commit the datasets to GitHub. Once again make sure to edit the `.gitignore` file so that it makes your repository ignore the files that comprise your chosen dataset.

### All About That ’Base (Draw Tables): Schema and Loader Files
With your dataset chosen, it’s time to populate a relational database with it:
1. Determine an appropriate logical schema for the dataset, in line with the database that will host it
2. Put that design in writing by providing a diagram of that schema, following the notation given in the [Super Basic Database Diagramming crib sheet](http://dondi.lmu.build/share/db/super-basic-database-diagramming.pdf): submit this as _schema.pdf_
3. Implement that schema in SQL DDL: submit this as _schema.sql_
4. Write one or more programs that will populate the target database with the dataset: submit these as one or more _loader_ source files

### SQL Me This, Caped Crusader: _queries.md_
Show off your ability to derive information from your database by writing the following SQL queries. For each query, use the format given in the [SQLFlix section](#sqlflix-netflix-praticemd-relational-database-edition) where you:
* State the criteria in English
* Provide the SQL query that yields those results
* Include a screenshot of this SQL query being issued in _psql_ alongside the first few results

Submit these in a Markdown file called _queries.md_. All queries should be _domain-appropriate_—i.e., they should make sense for an application that is trying to do real-world work with your adopted dataset:
1. A query that selects a subset of a particular entity in your dataset
2. Another such query, with a specific sort order `ORDER BY`
3. A query that combines information from more than one table using `INNER JOIN`
4. An _aggregate_ query that provides counts for certain groups in your dataset using `GROUP BY` and `COUNT`
5. A _ranking_ query that provides the “top” or “bottom” _n_ records based on some metric using `LIMIT`

If inspiration strikes you, don’t stop at just these five (5) queries. The more practice you get with SQL, the better. The five that are given are only meant to provide the base coverage for this assignment.

### Get ScanDALous: _dal.*_
“DAL” stands for “data access layer”—a term frequently used for the portion of a system whose primary concern is the CRUD (creation, reading, updating, and deletion) of persistent data. In a programming language of your choice (with help from a corresponding database connection library), write the beginnings of a data access layer for your database. The [Netflix Prize example](./netflix-prize-relational-example) provides its own _dal_ that you can use as a reference.

Since this is a mini-stack, we don’t expect your DAL to be full-featured. You only need to supply the following:
* Appropriate configuration and connection setup code
* Model objects and other definitions, as applicable (specifics will vary based on the language and database connection library)
* One (1) domain-appropriate _retrieval_ function that, given some set of arguments, will return corresponding data matching those arguments—you may adapt one of the queries you wrote in [SQL Me This, Caped Crusader](#sql-me-this-caped-crusader-queriesmd) for this—pick some aspect of that query that would make sense as parameters so that the same function can be used for multiple queries of the same type
* One (1) domain-appropriate “CUD” function (create, update, or delete) that modifies the database’s records, given some set of arguments

### Use the DAL, Luke
Write one (presumably short) program apiece that calls the retrieval and “CUD” functions, respectively. These programs’ primary jobs would be:
* Provide help on how to use the program
* Check program arguments for validity
* Call the underlying DAL function with those arguments
* Report any errors that may have occurred

Ultimately, these programs serve as “wrappers” to the DAL functions. The real magic happens in the DAL functions’ implementations. Again, refer to the [Netflix Prize example](./netflix-prize-relational-example) as needed.

## Operational Directives/Suggestions
- Make sure to divide the implementation work relatively evenly within your group. Most groups have four (4) members and there is plenty of work to spread around. Let each member “run point” on some set of tasks so that someone is on top of things but of course allow yourselves to help each other.
- Once more, do _not_ commit dataset files to the repository—they may be too large for that. Provide links instead. Edit _.gitignore_ to avoid accidental commits.
- Not everyone’s computer might have enough storage or other capacity—AWS is an option but watch your credits; or, designate someone as the “host” for doing work and find ways to collaborate over a screenshare and (friendly) remote control of a classmate’s screen.

## How to Turn it In
Commit everything to GitHub. Reiterating the deliverables, they are:
- [_netflix-practice.md_](#sqlflix-netflix-praticemd-relational-database-edition)
- [_about.md_](#game-dataset--match-aboutmd-gitignore)
- [_.gitignore_](#game-dataset--match-aboutmd-gitignore) (revised from what is already provided)
- [schema.pdf](#all-about-that-base-draw-tables-schema-and-loader-files)
- [schema.sql](#all-about-that-base-draw-tables-schema-and-loader-files)
- One or more [loader programs](#all-about-that-base-draw-tables-schema-and-loader-files)
- [_queries.md_](#sql-me-this-caped-crusader-queriesmd)
- [Data access layer (DAL) module](#get-scandalous-dal)
- Two (2) [DAL-calling programs](#use-the-dal-luke)

Review the instructions in the deliverables’ respective sections to see what goes in them.

## Specific Point Allocations
Work in progress—stay tuned!
