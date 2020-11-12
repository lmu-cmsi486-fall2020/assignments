**CMSI 486** Introduction to Database Systems, Fall 2020

# Assignment 1123
We wrap up our tour of selected database models with graph databases, as represented by [Neo4j](https://neo4j.com).

This assignment continues to have a similar structure as all of the mini-stack assignments. You are also to stay with the same group and dataset.

## Background Reading

### Theoretical/Conceptual Reading
Although graph _databases_ are a relatively recent development, the graph _data structure_ is well-studied. In many respects, a graph database is simply a persisted graph data structure. As such, Ullman’s [Foundations of Computer Science Chapter 9](http://infolab.stanford.edu/~ullman/focs/ch09.pdf) serves as a great refresher and reference on graphs and their associated algorithms.

Elmasri & Navathe’s NOSQL chapter 24 includes coverage of graph databases, also focusing on Neo4j as the reference system. If you don’t have the book, [this PDF](https://www.cs.purdue.edu/homes/bb/cs448_Fall2017/lpdf/Chapter24.pdf) covers the chapter, with graph database and Neo4j coverage appearing near the end.

### Technical/Operational Reading
Direct technical assistance for the action items in this assignment can be found primarily in the [Neo4j](https://neo4j.com/docs/) documentation site. Documentation types range from initial [Getting Started](https://neo4j.com/docs/getting-started/current/) tutorial to a full-blown [Operations Manual](https://neo4j.com/docs/operations-manual/current/).

Separate but similar are the [Neo4j Developer Guides](https://neo4j.com/developer/get-started/)—confusingly, these have overlapping content as the official docs but are distinct from them, and they have embedded videos if that suits your learning style better.

There isn’t an AWS-branded managed service for Neo4j, so the default approach of deploying one via EC2 applies. For this, Neo4j has [its own guide](https://neo4j.com/docs/operations-manual/current/cloud-deployments/neo4j-aws/) for doing so. There is also an [AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/Neo4j-Neo4j-Graph-Database-Community-Edition/B071P26C9D) for a prebuilt AMI (Amazon Machine Image) that already has it installed, with some guidance on estimated costs.

Neo4j shares MongoDB’s terminology choice of “drivers” as the name for libraries that allow general-purpose programs to communicate with a Neo4j server. [Multiple languages are supported](https://neo4j.com/developer/language-guides/) and for our [Netflix Prize graph database mini-stack case study](./netflix-prize-graph-example), examples are provided for [Python](https://neo4j.com/developer/python/) and [JavaScript](https://neo4j.com/developer/javascript/). If you choose to use [Java](https://neo4j.com/developer/java/), Neo4j also provides an [“OGM” library](https://neo4j.com/developer/neo4j-ogm/) (“Object Graph Mapper,” in the vein of “Object Relational Mapper”).

## For Submission: Graph Database Mini-Stack
For this assignment, you are asked to build the beginnings of a _graph database_ persistence layer for an envisioned application that is based on your chosen dataset. A working example of such a persistence layer is provided for our on-going Netflix Prize case study.

### NodeFlix: _netflix-pratice.md_, Graph Database Edition
Transfer some skills from the [Netflix Prize graph database mini-stack case study](./netflix-prize-graph-example): study the logical schema; study and run the given preprocessor programs and _import_ command so that you have the dataset in graph form (giving them ample time to finish!); study and run the sample programs to see how they and their respective libraries interact with Neo4j.

Due to the specific strengths of and motivations for graph databases, we change up our Netflix portion somewhat in order to emphasize these differentiating features. However, as before, make sure to still provide the following items for each in _netflix-practice.md_:
* State what the query/statement is asking or doing in English
* Provide the Neo4j Cypher query/statement that yields those results
* Include a screenshot of this query/statement being issued and the graph that it produces

**Watch for scale:** Graph databases require a _lot_ of resources. Watch out for queries that might return too many nodes and edges—if you seem to have formulated one, find ways to restrict it either with greater specifics or through the [`LIMIT`](https://neo4j.com/docs/cypher-manual/current/clauses/limit/) clause.

1. _Create new nodes and relationships_: Do some IMDB/Wikipedia research on your choice of artists (performers, directors, writers, musicians, etc.) who are affiliated with movies/shows in the Netflix dataset and connect them to those shows’ nodes with appropriate relationships. Pick a mix—around five (5) such nodes will be good, and make sure they have movies/shows in common, in different combinations. Research and define a small set of common properties for those artists, such as gender, birthdate, nationality, etc. Show the `MATCH`/`CREATE`/`RETURN` clauses that make these additions and a culminating query that produces a graph showing all of your additions and the movies/shows that they worked on (but no ratings—that would be too much).
2. _Viewers who are fans_: Let’s define a “fan” as someone who has rated a movie/show with a 5. Formulate a query that graphs the viewers who have given a 5 rating to the work of one of your selected artists. Make sure to return the viewers, the movies/shows that they rated, your chosen artist, and what they did in those movies/shows.
3. _Love/hate relationship_: Pick two movies that are likely to have a decent overlap of viewers. Formulate a query that graphs the viewers who all hated one movie (rated it a 1) but loved the other (rated it a 5).
4. _Watch party 1_: Define a set of criteria that filters out a small subset of movies/shows (no more than 3 to be safe). Formulate a query that produces a graph showing viewers who rated those movies/shows on the same day.
5. _Watch party 2_: Define a set of criteria that filters out a small subset of the artists that you’ve loaded into Neo4j. Formulate a query that produces a graph showing viewers who rated a movie/show on the same day, for movies/shows that your chosen artists worked on. Make sure to return the viewers, the movies/shows that they rated, the chosen artists, and what they did in those movies/shows.

For each of these queries, find ways to “sanity-check” your work—are there ways to run other queries that will help you verify whether you are really getting the results you’ve requested? It’s useful to do this at first while you’re still getting the hang of Cypher.

### Just _.gitignore_ It
Because this is your third go with the same dataset, we don’t need _about.md_ for this assignment. Just edit the `.gitignore` file again so that it makes your repository ignore your chosen dataset’s files.

### Rock the Graph-bah: Schema, Preprocessors, Headers, and Commentary
What doesn’t change from before is the need to populate your database with your dataset:
1. Determine an appropriate logical schema for the dataset—because this is a graph database, take the opportunity to rethink the structure of your data in a way that highlights relationships and connections within it
2. Put that design in writing by providing a diagram of that schema—follow the rounded-rectangle notation [used by Neo4j](https://neo4j.com/developer/guide-data-modeling/): submit this as _schema.*_ in some standard image format
3. Write one or more programs and header files that will populate the target database with the dataset using _neo4j-admin import_: submit these as _preprocess*_ and _*-header.csv_ files
4. In a Markdown file called _design.md_, provide commentary on your logical schema design choices with an embedded image or link to your schema diagram; in addition, provide the command sequence for loading up your dataset, with explanatory remarks as needed

### Dance the Graphy Q: _queries.md_
Show off your ability to derive graphs from your database by writing the following Cypher queries. For each query, use the format given in the [NodeFlix section](#nodeflix-netflix-praticemd-graph-database-edition) where you:
* State what the query/statement is asking or doing in English
* Provide the Neo4j Cypher query/statement that yields those results
* Include a screenshot of this query/statement being issued and the graph that it produces

Submit these in a Markdown file called _queries.md_. All queries should be _domain-appropriate_—i.e., they should make sense for an application that is trying to do real-world work with your adopted dataset:

1. A query that matches a meaningful subgraph in your dataset
2. Another such query, involving a different set of nodes, properties, and relationships
3. A query that matches a meaningful subgraph then [_optionally_ matches](https://neo4j.com/docs/cypher-manual/4.1/clauses/optional-match/) more relationships/nodes (i.e., the query returns all nodes in the first subgraph even if they don’t match the second pattern)
4. An _overall_ aggregate query that provides counts or other aggregate computations for an overall set of pattern-matched nodes or edges (this one will not return a graph)
5. A _grouped_ aggregate query that provides counts or other aggregate computations for groupings derived from pattern-matched nodes or edges (this one will not return a graph)

If inspiration strikes you, don’t stop at just these five (5) queries. The more practice you get with Cypher, the better. The five that are given are only meant to provide the base coverage for this assignment.

### Connect the DAL: _dal.*_
As with the other mini-stack assignments, we would like the beginnings of a graph database DAL. Once more, you may choose the programming language for this code—the only requirement is that a Neo4j “driver” exists in that language. The [Netflix Prize example](./netflix-prize-graph-example) again provides its own _netflix-dal_ that you can use as a reference:
* Appropriate configuration and connection setup code
* Model objects and other definitions, as applicable (specifics will vary based on the language and database connection library)
* One (1) domain-appropriate _retrieval_ function that, given some set of arguments, will return a graph matching those arguments—you may adapt one of the queries you wrote in [Dance the Graphy Q](#dance-the-graphy-q-queriesmd) for this—pick some aspect of that query that would make sense as parameters so that the same function can be used for multiple queries of the same type
* One (1) domain-appropriate “CUD” function (create, update, or delete) that modifies the database’s overall graph, given some set of arguments

One aspect where a graph database is at a disadvantage here is that the graph aspect only becomes clear with a graph rendering, which is highly infeasible with a command line program. You aren’t required to go that far in your demo programs, but make sure that your functions’ return values still contain enough information to produce a graph rendering. As long as your functions return collections of Neo4j’s “record” objects, a graph can still be constructed given the right front end.

### (:Program)-[:CALLS]->(:Dal)
Write one (presumably short) program apiece that calls the retrieval and “CUD” functions, respectively. These programs’ primary jobs would be:
* Provide help on how to use the program
* Check program arguments for validity
* Call the underlying DAL function with those arguments
* Report any errors that may have occurred

As mentioned in the [DAL instructions](#connect-the-dal-dal), it isn’t very feasible to expect a command-line program to provide a graph rendering (though it isn’t outright impossible; just…a helluva lot of work). Still, try to keep your output readable and clear. If you can express some of the graph aspects of the return value (e.g., listing connected nodes as indented beneath another node), feel free to give it a shot.

## Operational Directives/Suggestions
The same notes and suggestions remain from before:
- Make sure to divide the implementation work relatively evenly within your group. Most groups have four (4) members and there is plenty of work to spread around. Let each member “run point” on some set of tasks so that someone is on top of things but of course allow yourselves to help each other.
- Once more, do _not_ commit dataset files to the repository—they may be too large for that. Provide links instead. Edit _.gitignore_ to avoid accidental commits.
- Not everyone’s computer might have enough storage or other capacity—AWS is an option but watch your credits; or, designate someone as the “host” for doing work and find ways to collaborate over a screenshare and (friendly) remote control of a classmate’s screen.

## How to Turn it In
Commit everything to GitHub. Reiterating the deliverables, they are:
- [_netflix-practice.md_](#nodeflix-netflix-praticemd-graph-database-edition)
- [_.gitignore_](#just-gitignore-it) (revised from what is already provided)
- [_schema.*_](#rock-the-graph-bah-schema-preprocessors-headers-and-commentary)
- [Preprocessor program(s) and _*-header.csv_ files](#rock-the-graph-bah-schema-preprocessors-headers-and-commentary)
- [_design.md_](#rock-the-graph-bah-schema-preprocessors-headers-and-commentary)
- [_queries.md_](#dance-the-graphy-q-queriesmd)
- [Data access layer (DAL) module](#connect-the-dal-dal)
- Two (2) [DAL-calling programs](#program-calls-dal)

Review the instructions in the deliverables’ respective sections to see what goes in them.

## Specific Point Allocations
This assignment is scored according to outcomes _1a_, _1d_, _3a_–_3d_, and _4a_–_4f_ in the [syllabus](https://dondi.lmu.build/fall2020/cmsi486/cmsi486-fall2020-syllabus.pdf). For this particular assignment, graded categories are as follows:

| Category | Points | Outcomes |
| -------- | -----: | -------- |
| _netflix-practice.md_ correctly implements the requested operations | 5 points each, 25 points total | _1a_, _1d_, _3a_–_3c_, _4a_–_4d_ |
| _.gitignore_ correctly prevents accidental commits of dataset files | deduction only, if missed | _4a_ |
| _schema.*_ clearly diagrams the logical schema | 5 points | _1d_, _4c_ |
| Preprocessor program(s) and _*-header.csv_ files | 15 points | _3b_, _3c_, _4a_–_4d_ |
| _design.md_ explains the logical schema and import approach | 5 points | _1d_, _4c_ |
| _queries.md_ correctly implements the requested operations | 5 points each, 25 points total | _1d_, _3c_, _4a_–_4d_ |
| DAL module | 19 points total | _3c_, _3d_, _4a_–_4d_ |
| • Correct, well-separated configuration and setup | 5 points | |
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
