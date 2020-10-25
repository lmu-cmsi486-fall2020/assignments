**CMSI 486** Introduction to Database Systems, Fall 2020

# Netflix Prize Document Database Mini-Stack Example
This folder and README contains sample commands and code that correspond to what is being requested for the [Document-Centric Database Mini-Stack assignment](../README.md). To save repository space, the data files themselves are _not_ included here: before trying out these commands and programs, please [download the files](https://www.kaggle.com/netflix-inc/netflix-prize-data) into this folder first.

To avoid accidental committing of these files, a _.gitignore_ file has been placed here as well. We are definitely not taking an extra two gigabytes of repository space lightly!

## The Greater Schema of Things, Document Edition
The very premise of document-centric databases is to move away from data-as-tables to data-as-documents. Thus, the logical model of these systems bears more resemblance to conventional programming language data structures: objects, nested objects, arrays, nested arrays. Repeatable instances of these entities are _documents_ and these documents are stored in _collections_ (MongoDB) or _indices_ (Elasticsearch).

Document-centric databases also tend to be less restrictive in terms of _declaring_ your logical schema to the database. Both MongoDB and Elasticsearch allow for the addition of documents without previously defining what they will contain. However, Elasticsearch does work better if it _is_ given a schema (which it labels as the _mappings_ of an index).

On the other hand, the concept of a “join” across collections or indices within a single query is either very rare or not done at all. MongoDB has a `$lookup` operator which can do this in certain situations; Elasticsearch only allows it within documents of a single index (and highly discourages it nonetheless). The main alternative to this is to shift to nested arrays (which is what we have done here) but that isn’t always applicable. If it becomes necessary to associate documents from one collection/index with another, this has to be done as a second query. (another reason for abstracting these operations behind a DAL)

Both systems provide advice on how to structure the documents that are stored within them. This [design guide](https://docs.mongodb.com/guides/server/introduction/) provides some basics for MongoDB. The [Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html) section of Elasticsearch’s documentation is more of a reference, though it does provide some advice.

For the document-centric version of the Netflix case study, we leverage the more freeform approach of documents by _nesting_ a movie’s ratings within the movie document itself. Thus, our design only involves one collection or index, consisting of documents that look like this (note our use of a pseudo-JSON format to express our schema):

```
/* Collection/Index Name: movies */
{
  "id":    // Netflix-assigned movie identifier
  "year":  // Release year
  "title": // Title of movie/show

  "ratings": [
    // Ratings that were given to this movie/show
    {
      "viewer_id":  // Identifier of the viewer who gave this rating
      "rating":     // The rating value itself, from 1 to 5
      "date_rated": // The date the rating was given, in ISO-8601 format.
    }
  ]
}
```

MongoDB does not need to be explicitly told about this structure. Elasticsearch doesn’t technically need it either, but it _guesses_ the structure based on the first document that is loaded into it—and actually it guesses differently from what we prefer, particularly with respect to the nested _ratings_ array. Thus, we provide a partial schema so that it handles the _ratings_ array in a way that fits our anticipated queries better. Details are provided in the [Elasticsearch](./elasticsearch) implementation of our mini-stack.

### Correctness Still Matters
With new systems and new query approaches coming up, it’s important to note that the need to verify correctness doesn’t go away. Never lose sight of checking your queries against others, to make sure that the results you are getting are indeed the ones you’re expecting. This is especially true of aggregation queries, which can feel quite different due to our use of a nested _ratings_ array.

## Two Docs Diverge in a Yellow Wood
At this point, the two document-centric systems become quite distinct when it comes to loading up the data, performing queries, and programming a DAL for them. The broad strokes still apply—raw data must be loaded, queries are performed using some language defined by the system, and libraries allow programmatic interaction with a server—but the specifics differ. Thus, we find ourselves going to the specific [MongoDB](./mongodb) and [Elasticsearch](./elasticsearch) folders sooner than with previous systems.
