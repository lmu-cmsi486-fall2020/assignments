# A MongoDB Mini-Stack for the Netflix Prize Data
Operationally, interacting with MongoDB at the command line feels a lot like other systems—you run the command, get a MongoDB-specific prompt, then issue commands. Some commands are purely for getting around, while others officially comprise MongoDB’s “query language.”

Speaking of which, MongoDB’s “language” feels a lot like calling functions. Parameters are provided as objects, written out in JavaScript/JSON style. The output is similarly JSON-y, and in that respect MongoDB may feel harder to read in plain text than a tabular display.

MongoDB does have an official GUI in the form of [Compass](https://www.mongodb.com/products/compass)—that’s available for you to use, but for this document we will stay consistent with all other systems and interact with MongoDB as directly as possible.

## Schema Gets Doc’ed—Straight to Loading
MongoDB doesn’t require a schema to get started: you start adding documents to a collection and go. However, some planning still helps, which is why [writing out the anticipated JSON structure of your documents](../#the-greater-schema-of-things-document-edition) remains called for. Having done that, we are in a position to write out our loaders.

MongoDB comes with a utility called [_mongoimport_](https://docs.mongodb.com/guides/server/import/) which is supposed to represent the most efficient possible way to load data into MongoDB. Observing here that the vast majority of our data is made up of ratings, we’ll take the strategy if using _mongoimport_ for the ratings in order to take advantage of _mongoimport_’s performance.

Because we’re modeling ratings as arrays nested within movie documents, that means we’ll create the movie documents with _just the ratings_ first, then populate their years and titles later:

    python3 rating_loader.py | mongoimport --db netflix --collection movies --drop --host=localhost

(the `--host` argument isn’t strictly necessary because the default is `localhost` but we include it here for completeness)

Similarly to other loaders you’ve seen, this one can be “previewed” by running `python3 rating_loader.py` by itself. This will send the _mongoimport_-ready data to _stdout_. If this output looks good to you, you can then append the piped portion and off it goes. Comparatively speaking, _mongoimport_ was around seven (7) times faster than the `INSERT`-based rating loader seen in the relational database mini-stack. (of course, this isn’t an apples-to-apples comparison—there are also “bulk load” approaches for relational databases which will likely be pretty competitive in terms for performance—but these are product-specific and less portable)

Once we have our “movie documents” consisting of just _id_ and _ratings_ loaded up, the approach used by the movie loader is to now perform `updateOne` calls on the collection in order to set the movies’ _year_ and _title_—these need to be sent as commands to the _mongo_ program. As the loader scans the _movie_titles.csv_ file, it builds an `updateOne` invocation for each movie that includes its year and title:

    python3 movie_loader.py | mongo mongodb://localhost

As with the rating loader, you can run `python3 movie_loader.py` by itself first in order to see the output—this is effectively the sequence of commands that we will ask _mongo_ to perform. Piping this to `mongo mongodb://localhost` then performs the updates for real.

### MongoDB-DB-Do-overs
You might have noticed the `--drop` argument in the _mongoimport_ command above: this ensures that the collection is always “dropped” (deleted) whenever the import happens. This helps when still perfecting the loading scheme for a given dataset.

To manually do things over, you can use the `dropDatabase` method within _mongo_:

    use <database name>
    db.dropDatabase()

These are useful in the early going, but as always, use with caution! These aren’t undoable (unless you run regular backups of the database files).

## Sample Queries
Although the concepts are the same for querying across most database types, the _language_ for such queries varies widely. MongoDB tries to help here by supplying a [mapping chart](https://docs.mongodb.com/manual/reference/sql-comparison/) that “translates” SQL ideas into MongoDB. This can be a handy first stop in figuring out how to express a certain query the MongoDB way. For “pure” MongoDB learning, the [Query Documents](https://docs.mongodb.com/manual/tutorial/query-documents/) tutorial works well as a start.

### Basic Matching and Logical Combinations
The workhorse of MongoDB querying is its collections’ `find` method. `find` accepts a two objects, whose content and structure determine all of the desired behavior for the operation. The first object is the _query_—it determines _which_ documents are to be retrieved. The second object is the _projection_—it determines which _parts_ of which documents should be returned. (MongoDB takes the term “projection” from the relational algebra, which originated this term as the operation for extracting a subset of columns from a table or relation)

All queries assume that `use <database name>` has already been invoked in _mongo_ so that the current database is the one whose collections you want to query.

* List movies containing both `'and'` and `'of'` in their titles, sorted ascending by year then title:
```javascript
db.movies.find({
  $and: [
    { title: / and / },
    { title: / of / }
  ]
}, {
  _id: 0, id: 1, year: 1, title: 1
}).sort({
  year: 1, title: 1
})
```
```json
{ "id" : "3790", "title" : "Avant-Garde: Experimental Cinema of the 1920s and '30s", "year" : 1921 }
{ "id" : "2449", "title" : "The Private Lives of Elizabeth and Essex", "year" : 1939 }
{ "id" : "12416", "title" : "Sherlock Holmes and the Voice of Terror", "year" : 1942 }
{ "id" : "7220", "title" : "Anna and the King of Siam", "year" : 1946 }
{ "id" : "17715", "title" : "The Adventures of Ma and Pa Kettle: Vol. 1", "year" : 1947 }
  ...
  ...
```
`$and` and `$or` do what you expect, and they take arrays of additional conditions. This gives these booleans a prefix- rather than infix- look.

The `_id` property is the internal MongoDB ID, which needs to be explicitly omitted (as opposed to _ratings_, which gets omitted solely by not being mentioned in the projection object).

* List movie titles released in the 20th century with the substring `'future'` in their titles, case-insensitively, sorted ascending by title:
```javascript
db.movies.find({
  $and: [
    { title: /future/i },
    { year: { $lt: 2001 } }
  ]
}, {
  _id: 0, title: 1
}).sort({
  title: 1
})
```
```json
{ "title" : "Back to the Future" }
{ "title" : "Back to the Future Part II" }
{ "title" : "Back to the Future Part III" }
{ "title" : "Future War" }
{ "title" : "Futuresport" }
{ "title" : "Ivan Vasilievich: Back to the Future" }
{ "title" : "Megaman: Battle for the Future" }
{ "title" : "The X-Files: Fight the Future" }
```
The usual comparators are also available, but they look very different due to the JSON format—e.g., `$lt` above. Plus, the built-in regex expression support also handles options right after the `/ /` delimiters, such as case-insensitivity.

### Nested Objects and Aggregations
[Aggregations in MongoDB](https://docs.mongodb.com/manual/aggregation/) are distinct from queries: they use the `aggregate` method which takes in an _array_ rather than an object. Each element of the array represents a step in an overall _pipeline_ which works from the collection, narrowing down the documents to use in the aggregation, to finally the aggregation/grouping that you want to perform.

* Determine the average rating given by all viewers on the month of October, 2004:
```javascript
db.movies.aggregate([
  { $unwind: '$ratings' },
  {
    $match: {
      $and: [
        { 'ratings.date_rated': { $gte: '2004-10-01' } },
        { 'ratings.date_rated': { $lte: '2004-10-31' } }
      ]
    }
  },
  {
    $group: {
      _id: null,
      average: { $avg: '$ratings.rating' }
    }
  }
])
```
```json
{ "_id" : null, "average" : 3.6811938432580797 }
```
This aggregation has three stages: `$unwind`, `$match`, and `$group`. The `$unwind` stage first “pulls out” (i.e., “unwinds”) the nested _ratings_ arrays of each movie so that we can perform an aggregation on them, independent of the movie. The `$match` stage then states _which_ of these ratings we want to use, much like a query. Finally, the `$group` stage performs the aggregation. When aggregating over an entire collection, we supply a null `_id`. Otherwise, the `_id` would hold the values over which we want to perform the grouping.

* List the titles of movies that got a rating of 1 on December 25, 2002, sorted ascending by title:
```javascript
db.movies.find({
  ratings: {
    $elemMatch: {
      rating: 1,
      date_rated: '2002-12-25'
    }
  }
}, {
  _id: 0, title: 1
}).sort({
  title: 1
})
```
```json
{ "title" : "102 Dalmatians" }
{ "title" : "13 Conversations About One Thing" }
{ "title" : "3000 Miles to Graceland" }
{ "title" : "A Couch in New York" }
{ "title" : "A Fish Called Wanda" }
  ...
  ...
```
Note that this one isn’t an aggregation but a query over the rating documents nested within each movie’s _ratings_ array. The `$elemMatch` operator is used to pick out documents whose nested array includes at least one element that matches the given conditions.

* List the year and rating count for movies released before 1910 or after 2000, sorted descending by year:
```javascript
db.movies.aggregate([
  {
    $match: {
      $or: [
        { year: { $lt: 1910 } },
        { year: { $gt: 2000 } }
      ]
    }
  },
  {
    $group: {
      _id: '$year',
      count: { $sum: { $size: '$ratings' } }
    }
  },
  {
    $sort: {
      _id: -1
    }
  }
])
```
```json
{ "_id" : 2005, "count" : 1983802 }
{ "_id" : 2004, "count" : 10456339 }
{ "_id" : 2003, "count" : 9576604 }
{ "_id" : 2002, "count" : 8640932 }
{ "_id" : 2001, "count" : 7241888 }
{ "_id" : 1909, "count" : 109 }
{ "_id" : 1896, "count" : 152 }
```
Because we need counts per year, we’re back to using `aggregate` rather than `find`. We’re aggregating over movies now so we don’t `$unwind`, but we do `$group` by `$year` (note the `$` prefix required by MongoDB when referencing a field in the document) and the `$sort` operation is part of the pipeline rather than something that is done after the aggregation results are returned.

## DAL Details
With MongoDB’s very strong affinity to JSON, JavaScript is a good fit for a MongoDB DAL (although other language options are [certainly viable](https://docs.mongodb.com/drivers/)—gotta pick one though). The [official MongoDB “driver” for JavaScript/Node.js](https://docs.mongodb.com/drivers/node/) is well-documented, including a [Quick Start](https://docs.mongodb.com/drivers/node/quick-start) (although this DAL code somewhat takes its place as something that matches our context better), tutorial-style [Fundamentals](https://docs.mongodb.com/drivers/node/fundamentals), recipe-like [Examples](https://docs.mongodb.com/drivers/node/usage-examples), and finally a [reference](http://mongodb.github.io/node-mongodb-native/3.6/api/) firehose, among other sections. Have at it!

Due to its relative simplicity—and to make the library dependencies more explicit to you since you have to type them in yourself—our DAL example doesn’t come with a _package.json_. Instead, you can install the needed library directly within [this folder](.):

    cd mongodb # Within this repository
    npm install mongodb

The DAL code is structured like the other mini-stacks: _netflix-dal.mjs_ is the data access layer itself, with its setup code and DAL functions. The remaining programs are mini-applications that demonstrate one DAL function each. You’ll notice that these programs are very similar to their equivalents in other mini-stacks—but they aren’t _completely_ identical due to specific behaviors or features in MongoDB. Study the code and read their comments to learn about what makes this DAL (and its functions) different from others.

Like our other DALs, we separate configuration information from the code. As before, just set the `DB_URL` variable prior to invoking at DAL-using program:
    
    DB_URL=<database URL> node <program name> <arguments>

So, running _add-movie.mjs_ for a MongoDB server on your local machine would look like this:

    DB_URL=mongodb://localhost node add-movie.mjs "Bill & Ted Face the Music" 2020
