**CMSI 486** Introduction to Database Systems, Fall 2020

# Assignment 1109
For this assignment, we shift our attention to one of the most prominent alternatives to the relational model—a document-centric database. You may choose between two such systems for this assignment: [MongoDB](https://www.mongodb.com) or [ElasticSearch](https://www.elastic.co/elasticsearch/).

As mentioned previously, this assignment has a similar structure to all of the mini-stack assignments. You are also to stay with the same group and dataset.

## Background Reading
At this point, the presumption is that you know your chosen dataset quite well, and of course the Netflix Prixe dataset continues to tag along. All reading is thus centered on what differentiates document-centric databases from the rest.

### Theoretical/Conceptual Reading
Unlike the relational database model, document-centric databases don’t have pre-established mathematical/theoretical underpinnings. There are lots of papers _about_ MongoDB and ElasticSearch (a quick look at the [ACM Digital Library](https://dl.acm.org) bears this out) but nothing like Ted Codd’s [seminal paper](https://dl.acm.org/doi/10.1145/362384.362685).

Chapter 24 of the Elmasri & Navathe textbook covers NoSQL systems in general (now represented in all-caps “NOSQL” to mean _Not Only_ SQL instead of flat-out **”no”** SQL). If you don’t have the book, [this PDF](https://www.cs.purdue.edu/homes/bb/cs448_Fall2017/lpdf/Chapter24.pdf) covers the chapter with some pages looking specifically at MongoDB.

### Technical/Operational Reading
Direct technical assistance for the action items in this assignment can be found primarily in the [MongoDB](https://docs.mongodb.com/manual/) and [ElasticSearch](https://www.elastic.co/guide/index.html) documentation sites. Watch out when doing web searches—multiple documentation sites exist for various versions of these systems so make sure that you are looking at documentation that matches the version you’re using. (this was also true of PostgreSQL but was less of an issue there because of SQL’s existence as a broader standard)

MongoDB has a separate collection of [Getting Started guides](https://docs.mongodb.com/guides/) which summarizes the fundamentals. ElasticSearch has a step-by-step [Getting Started](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html) set of pages as well. An [ElasticSearch video collection](https://www.elastic.co/videos/) is also available if this matches your learning style better.

Because there aren’t any managed services on AWS (that I know of) which specifically target MongoDB nor ElasticSearch, installing and running these on AWS are pretty much the same doing it on your own computer, except you’d be on an EC2 instances. That said, there are some official tips pages on how to set things up more optimally. These are likely above our pay grade but may be of interest to some of you anyway: [MongoDB on AWS](https://aws.amazon.com/quickstart/architecture/mongodb/) is by AWS itself and [Running ElasticSearch on AWS](https://www.elastic.co/blog/running-elasticsearch-on-aws) is the official recommendation from ElasticSearch (though its age may necessitate some tweaks).

We are also more strongly-bound to libraries that _specifically_ target these systems. MongoDB calls them “drivers.” ElasticSearch calls them “clients.” Whatever—they are libraries that you can use to write code that interacts with those respective systems. Pick a language, any language:
* [MongoDB driver (library) page](https://docs.mongodb.com/drivers/)
* [ElasticSearch client (library) listing](https://www.elastic.co/guide/en/elasticsearch/client/index.html)

Between these and the [Netflix Prize document-centric database mini-stack case study](./netflix-prize-document-example), the hope is that you have plenty of resources for getting into the system of your choice.

## For Submission: Document-Centric Database Mini-Stack
For this assignment, you are asked to build the beginnings of a _document-centric database_ persistence layer for an envisioned application that is based on your chosen dataset. A working example of such a persistence layer is provided for our on-going Netflix Prize case study.

### DocFlix: _netflix-pratice.md_, Document-Centric Database Edition
Transfer some skills from the [Netflix Prize document-centric database mini-stack case study](./netflix-prize-document-example): study the logical schema; study and run the given loader programs so that you have the dataset in document-centric form (giving them ample time to finish!); study and run the sample programs to see how they and their respective libraries interact with MongoDB and ElasticSearch.

With that background in mind, implement the queries listed below, providing the following items for each in _netflix-practice.md_:
* State the criteria in English
* Provide the MongoDB or ElasticSearch query that yields those results
* Include a screenshot of this query being issued in the corresponding direct-database access utility (_mongo_, _curl_, Postman) alongside the first few results

**Precision is the thing:** Due to the way document-centric databases work, it won’t always be possible to enforce the same level of precision that we see in other types of databases—but we can get close enough. Make a good-faith effort at eliminating extraneous information. If the request is for “the number of reviews” that meet a certain condition, don’t provide a query that lists the reviews and requires the user to look at how many reviews were returned; _the result itself_ must provide the number directly. Similarly, for queries that ask for the “highest” or “lowest” values of something, don’t make the user to look for the desired result manually—again, the query clearly identify the requested values.

1. _Movies filtered by title and/or year_: A query that retrieves the _ID_, _year_, and _title_ of movies that fit criteria of your choosing (e.g., movies with certain titles or title patterns, movies released on one or more given years, etc.), sorted ascending by _title_
2. _Number of movies released per year_: A query that takes movie criteria of your choosing and returns a collection consisting of _year_ and _count_ where _count_ is the number of movies that meet these criteria which were released on that _year_, sorted ascending by _year_
3. _Years with the most movies released_: A query that takes movie criteria of your choosing and returns the same collection as above except it only returns the _year_ and _count_ of the _top five (5) years_ with the most movies released, sorted descending by _count_ then ascending by _year_ in case of a tie
4. _Movies rated a certain way by a specific user_: A query that lists the _title_ and _year_ of movies seen by a particular user with a rating matching conditions of your choosing (e.g., 4 and above, 2 and below, etc.) sorted ascending by _title_
5. _Average rating of movies_: A query that takes movie criteria of your choosing and returns a collection consisting of _title_, _year_, and _avg_ where _avg_ is the average rating received by each movie, sorted descending by _avg_ (thus listing the top-rated movie first) then ascending by _title_ in case of a tie
6. _Specific average rating of movies_: A query that takes movie criteria of your choosing and returns a collection consisting of _title_, _year_, and _avg_ where _avg_ is the average rating received by each movie _and_ meeting some condition of your choosing such as average greater than 4, average less than 3, etc.—the results should be sorted descending by _avg_ (thus listing the top-rated movie first) then ascending by _title_ in case of a tie
7. _Number of reviews received by a movie during a certain time period_: A query that takes movie criteria of your choosing and returns a collection consisting of _title_, _year_, and _count_ where _count_ is the number of reviews received by each movie _within a particular date range_ of your choosing such as after 2005, during the month of September, etc.—the results should be sorted descending by _count_ (thus listing the most-frequently-rated movie first) then ascending by _title_ in case of a tie

For each of these queries, find ways to “sanity-check” your work—are there ways to run other queries that will help you verify whether you are really getting the results you’ve requested? It’s useful to do this at first while you’re still getting the hang of your chosen system’s query language.

### Just _.gitignore_ It
Because we’re on the same dataset as before, we don’t need _about.md_ for this assignment. Just edit the `.gitignore` file again so that it makes your repository ignore the files that comprise your chosen dataset.

### We Will, We Will Doc You: Schema and Loader Files
What doesn’t change from before is the need to populate your database with your dataset:
1. Determine an appropriate logical schema for the dataset, in line with the database that will host it—for document-centric databases, this is technically not necessary but we’ll still require it because we aren’t loading arbitrary data structures either
2. Put that design in writing by providing a diagram of that schema—notation is less rigid here again because of the way document-centric databases operate:
    * For MongoDB, state the chosen name for your database and the collections it will contain
    * For ElasticSearch, state the names of the indices that you will use
    * In both cases, describe the documents that will go into these collections or indices by _showing their JSON structure_—what are their property names? What types do they have? Are there any sub-objects or arrays?
    * Submit this as _schema.pdf_ or _schema.md_, as appropriate
3. For ElasticSearch, you may need to supply _mappings_ objects (one per index that requires _mappings_): if so, supply them as _**(index-name)**-mappings.json_ (meant for direct `PUT` via _curl_ or Postman to the intended index)
4. Write one or more programs that will populate the target database with the dataset: submit these as one or more _loader_ source files

### What’s Up Doc? _queries.md_
Show off your ability to derive information from your database by writing the following SQL queries. For each query, use the format given in the [DocFlix section](#docflix-netflix-praticemd-document-centric-database-edition) where you:
* State the criteria in English
* Provide the query that yields those results
* Include a screenshot of this query being issued in the corresponding direct-database access utility (_mongo_, Kibana) alongside the first few results

Submit these in a Markdown file called _queries.md_. All queries should be _domain-appropriate_—i.e., they should make sense for an application that is trying to do real-world work with your adopted dataset:
1. A query that selects a subset of a particular entity in your dataset
2. Another such query, with a specific sort order
3. _Either_ a sequence of queries that combines information from more than one collection (this may require some pseudocode that connects one collection to another) _or_ a query that iterates through nested collections or sub-objects
4. An _aggregate_ query that provides counts or other aggregate computations for certain groups in your dataset
5. A _ranking_ query that provides the “top” or “bottom” _n_ documents based on some metric

If inspiration strikes you, don’t stop at just these five (5) queries. The more practice you get with your chosen system’s query language, the better. The five that are given are only meant to provide the base coverage for this assignment.

### DAL-Doc-ahedron: _dal.*_
As with the other mini-stack assignments, we would like the beginnings of a document-centric DAL. Once more, you may choose the programming language for this code—the only requirement is that a “driver” (MongoDB) or “client” (ElasticSearch) exists for the corresponding system in that language. The [Netflix Prize example](./netflix-prize-document-example) again provides its own _dal_ that you can use as a reference:
* Appropriate configuration and connection setup code
* Model objects and other definitions, as applicable (specifics will vary based on the language and database connection library)
* One (1) domain-appropriate _retrieval_ function that, given some set of arguments, will return corresponding data matching those arguments—you may adapt one of the queries you wrote in [What’s Up Doc?](#whats-up-doc-queriesmd) for this—pick some aspect of that query that would make sense as parameters so that the same function can be used for multiple queries of the same type
* One (1) domain-appropriate “CUD” function (create, update, or delete) that modifies the database’s documents, given some set of arguments

A fun self-challenge here would be to see if you can implement _the exact same functions_ with _the exact same signatures and external behavior_ as your previous mini-stack. The benefit of doing this would be that you wouldn’t need to rewrite your demo applications (the next section). Because sometimes, this won’t be possible out of no fault of your own—some definitions may be inapplicable, the technology may shift, etc.—it wouldn’t be fair to offer extra credit for this; the main motivation would be to not have to write new [demo application code](#dal-call).

### DAL Call
Write one (presumably short) program apiece that calls the retrieval and “CUD” functions, respectively. These programs’ primary jobs would be:
* Provide help on how to use the program
* Check program arguments for validity
* Call the underlying DAL function with those arguments
* Report any errors that may have occurred

As mentioned in the [DAL instructions](#dal-doc-ahedron-dal), see if you can find a way to define your DAL so that the programs you submitted previously will work _without modification_. The reward would be that you don’t have to redo these programs! (but don’t worry about it if this isn’t feasible)

## Operational Directives/Suggestions
The same notes and suggestions remain from before:
- Make sure to divide the implementation work relatively evenly within your group. Most groups have four (4) members and there is plenty of work to spread around. Let each member “run point” on some set of tasks so that someone is on top of things but of course allow yourselves to help each other.
- Once more, do _not_ commit dataset files to the repository—they may be too large for that. Provide links instead. Edit _.gitignore_ to avoid accidental commits.
- Not everyone’s computer might have enough storage or other capacity—AWS is an option but watch your credits; or, designate someone as the “host” for doing work and find ways to collaborate over a screenshare and (friendly) remote control of a classmate’s screen.

## How to Turn it In
Commit everything to GitHub. Reiterating the deliverables, they are:
- [_netflix-practice.md_](#docflix-netflix-praticemd-document-centric-database-edition)
- [_.gitignore_](#just-gitignore-it) (revised from what is already provided)
- [_schema.pdf_/_schema.md_](#we-will-we-will-doc-you-schema-and-loader-files) and [_**(index-name)**-mappings.json_](#we-will-we-will-doc-you-schema-and-loader-files) (if applicable)
- One or more [loader programs](#we-will-we-will-doc-you-schema-and-loader-files)
- [_queries.md_](#whats-up-doc-queriesmd)
- [Data access layer (DAL) module](#dal-doc-ahedron-dal)
- Two (2) [DAL-calling programs](#dal-call)

Review the instructions in the deliverables’ respective sections to see what goes in them.

## Specific Point Allocations
This assignment is scored according to outcomes _1a_, _1d_, _3a_–_3d_, and _4a_–_4f_ in the [syllabus](https://dondi.lmu.build/fall2020/cmsi486/cmsi486-fall2020-syllabus.pdf). For this particular assignment, graded categories are as follows:

| Category | Points | Outcomes |
| -------- | -----: | -------- |
| _netflix-practice.md_ correctly implements the requested operations | 4 points each, 28 points total | _1a_, _1d_, _3a_–_3c_, _4a_–_4d_ |
| _.gitignore_ correctly prevents accidental commits of dataset files | deduction only, if missed | _4a_ |
| _.schema.pdf_/_schema.md_ and _**(index-name)**-mappings.json_ (if applicable) | 5 points | _1d_, _4c_ |
| Loader program(s) | 15 points | _3b_, _3c_, _4a_–_4d_ |
| _queries.md_ correctly implements the requested operations | 5 points each, 25 points total | _1d_, _3c_, _4a_–_4d_ |
| DAL module | 21 points total | _3c_, _3d_, _4a_–_4d_ |
| • Correct, well-separated configuration and setup | 7 points | |
| • Domain-appropriate retrieval function | 7 points | |
| • Domain-approprate “CUD” function | 7 points | |
| DAL-calling programs | 3 points each, 6 points total | _3d_, _4a_–_4d_ |
| Hard-to-maintain or error-prone code | deduction only | _4b_ |
| Hard-to-read code | deduction only | _4c_ |
| Version control | deduction only | _4e_ |
| Punctuality | deduction only | _4f_ |
| **Total** | **100** |

Where applicable, we reinterpret outcomes _4b_ and _4c_ in this assignment to represent the clarity, polish, and effectiveness of how you document your dataset, database, and its features, whether in written descriptions, the database diagram, or the DAL code.

Note that inability to compile and run any code to begin with will negatively affect other criteria, because if we can’t run your code (or commands), we can’t evaluate related remaining items completely.
