# An Elasticsearch Mini-Stack for the Netflix Prize Data
Interacting with Elasticsearch directly will need some adjustment—instead of a command-line interface, Elasticsearch’s “commands” are all delivered as web requests. Yes, there are user interfaces available that go on top of that ([Kibana](https://www.elastic.co/kibana) being their own home-grown offering), but the fact of the matter remains that this is a cleanly-delineated layer.

As such, you will want to have some familiarity with a client that “speaks” web requests. _curl_ is a command line option and is very convenient as long as you know how to pick the method to use, set headers, and populate its payload—this last aspect is particularly important for data loading. If you’re working with smaller chunks of data, [Postman](https://www.postman.com) is the more approachable tool—you still need to know your web request basics but once you do, making requests is quite straightforward.

## Initialization: Mappings and Settings
As mentioned in the [overview](..), Elasticsearch doesn’t overtly require a schema but it _does_ attempt to guess one once documents are loaded to an index. Its guesses can sometimes be accurate, but sometimes an override is called for. This is the case for our nested _ratings_ array: Elasticsearch’s default approach to handling arrays doesn’t correspond to how we want to use _ratings_, so we must start by setting a _mappings_ object for our _movies_ index before we do any work.

**This is one major caution with Elasticsearch:** Once an index has documents loaded, the _mappings_ object _cannot_ be changed. It’s flat-out necessary to delete an index and start it over with a new _mappings_ definition if you realize that your mappings have to change. While still finalizing how to use your dataset, keep your loader programs handy and see if you can work with a subset of the data first, in case you need to start over with an index.

Back to our dataset, we will want to treat our _ratings_ objects as `nested`—in other words, we want to retain their structures as objects. The [`nested` field type page](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html) describes the distinction between “flattened” arrays (the default Elasticsearch behavior) and `nested` ones (what we want here).

Thus, we start our _movies_ index by setting (`PUT`ting) the `mappings` object defined in [_movies-mappings.json_](./movies-mappings.json):

```http
PUT http://localhost:9200/movies
```
```json
{
  "mappings": {
    "properties": {
      "ratings": {
        "type": "nested"
      }
    }
  }
}
```

The size of our dataset also necessitates a change in _settings_—settings are what you’d expect: various configuration values that customize the behavior of an index. It turns out that nested arrays have a maximum size—and our dataset exceeds the default. So we change the setting—that’s what settings are for, after all:

```http
PUT http://localhost:9200/movies/_settings
```
```json
{
  "index.mapping.nested_objects.limit": 250000
}
```

### Ctrl-Alt-`DELETE` Method
When there’s a need to start over, you’ll want to use the `DELETE` method on your index’s URL. Handy when needed—but use with caution!

```http
DELETE http://localhost:9200/movies
```

## Doc and Load
Time to load up the index! We load in two phases: first, we send the movies (without ratings) to the index, then we’ll load the ratings into each movie.

### The Incredible *_bulk*
For [_movie_loader.py_](./movie_loader.py), we make use of an index’s [*_bulk* endpont](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html): sort of a “shortcut” endpoint that can take a large chunk of JSON representing multiple documents.

*_bulk* does have its limits, but fortunately our _movie_titles.csv_ file is within those limits. If this turned out to be too large for a single *_bulk* call, we would need to write some code the break up the output into more digestible chunks.

Your can run [_movie_loader.py_](./movie_loader.py) all by itself to see what *_bulk*’s payload looks like:

    python3 movie_loader.py

When you’re ready to load for real, we just pipe its output to an invocation of _curl_ that invokes *_bulk* with payload coming from standard input:

    python3 movie_loader.py | curl -H "Content-Type: application/json" -XPOST "localhost:9200/movies/_bulk?pretty&refresh" --data-binary @-

The `pretty` parameter formats the resulting response for human readability; the `refresh` parameter tells Elasticsearch to make the loaded data available _immediately_—if you’re curious about that, you can [read some details here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-refresh.html).

### Rated R for _requests_
The *_bulk* endpoint won’t work for ratings because we’re _nesting_ the ratings as arrays within each movie document. Because this approach means that loading ratings will _update_ each movie document, we’ll instead use the [*_update*](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html) endpoint. Further, because we’re only updating _part_ of the movie documents—i.e., we don’t want to wipe out the attributes that are already there—we’ll use the variant that performs a [partial update](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html#_update_part_of_a_document).

This approach means that we’ll need to gather up the entire list of ratings per movie. Fortunately, our overall structure for processing the _combined_data_ files still holds, except this time, we build up all of the ratings for a given movie into one array. Then, we send that array to *_update*.

This approach means that we need to make our *_update* requests _within_ the [_rating_loader.py_](./rating_loader.py) program. To do this, we use the Python _requests_ library. Thus, _rating_loader.py_ needs a virtual environment so that we can install _requests_:

    cd elasticsearch # Within this repository
    python3 -m venv env
    source env/bin/activate
    pip3 install requests

Once that’s done (and the _combined_data_ files are present), it’s a matter of running the program:

    python3 rating_loader.py

Contrary to what one might expect from a loader that uses web requests to do its work, the _rating_loader.py_ compares well in performance to movie creation (via ratings) with _mongoimport_. Both loaders appear to perform very similarly—around seven (7) times faster than the `INSERT`-based relational database loader. One wonders how the relational database loader would compare if its approached were changed from `INSERT` statements to something more suited to bulk loading.

## Sample Queries
Because Elasticsearch is document-centric, it returns, well…documents. All queries are done via the [*_search* endpoint](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html), and Elasticsearch’s “query language” consists of specially-formatted JSON payloads.

Query conditions go in a `query` object within the *_search* payload. This so-called [“Query DSL”](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html) (domain-specific language) is quite a beast—we highlight examples here but be aware that there’s a _lot_ more available.

Because we are embedding _ratings_ in each movie, Elasticsearch’s default behavior of returning the entire document can be unwieldy—thus, we use the [`_source` property](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html) to omit the _ratings_ array when desired.

Elasticsearch is conservative about the default number of results that it returns for a query. Thus, [pagination parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html) may be needed more often than in other databases. Put simply, this consists of a `from` property to indicate where to start and a `size` property to indicate how many results to return. Both properties are peers of the `query` object in the payload.

Because Elasticsearch’s primary function is document search, it has a unique “free” feature—it provides a _relevance score_ for its search results, and by default it will sort by relevance. Manual sorting remains available, but due to this distinctive behavior, it will also be interesting to see what the score-based sorting may be for the queries that you write. This is actually Elasticsearch’s _raison d’être_, and to some degree we are giving it short shrift because we’re approaching Elasticsearch as “just” a database here. Worth exploring further if it’s your cup of tea 🍵

### Basic Matching and Logical Combinations
The [`match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html) and [`bool`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html) constructs are good starting points—`match` defines text-matching or equality conditions, and `bool` helps to combine these conditions (and other conditions as well).

All text-matching queries in Elasticsearch are _case-insensitive_ by default—indeed, if you want to allow case-sensitive searching, you _actually have to plan for this ahead of time_ and include this customization in the _mappings_. We didn’t bother to do this which is why some of the results you’ll see may differ from what was seen in other databases.

To sort manually (i.e., not by relevance), a `sort` property can be specified as a peer of `query`. As you’ll see from the results, the sort fields are _repeated_ in a `sort` array—thus, in some cases, you can potentially _skip the documents entirely_ (`_source: false`) if the only data you want are wholly contained in the `sort` fields.

* List movies containing both `'and'` and `'of'` in their titles, sorted ascending by year then title:
```http
GET http://localhost:9200/movies/_search?pretty
```
```json
{
  "_source": {
    "excludes": ["ratings"]
  },
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "and" } },
        { "match": { "title": "of" } }
      ]
    }
  },
  "sort": ["year", "title.keyword"]
}
```
Here’s a subset of the response:
```json
{
  "_index": "movies",
  "_type": "_doc",
  "_id": "3790",
  "_score": null,
  "_source": {
    "year": 1921,
    "title": "Avant-Garde: Experimental Cinema of the 1920s and '30s"
  },
  "sort": [
    1921,
    "Avant-Garde: Experimental Cinema of the 1920s and '30s"
  ]
},
{
  "_index": "movies",
  "_type": "_doc",
  "_id": "10827",
  "_score": null,
  "_source": {
    "year": 1939,
    "title": "Of Mice and Men"
  },
  "sort": [
    1939,
    "Of Mice and Men"
  ]
},
```
Fun exercise: remove the `sort` to see what the _ranked_ order looks like.

We enlist [`range`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html) when we want to specify conditions with numbers and dates:

* List movie titles released in the 20th century with the substring `'future'` in their titles, case-insensitively, sorted ascending by title:
```http
GET http://localhost:9200/movies/_search?pretty
```
```json
{
  "_source": {
    "excludes": ["ratings"]
  },
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "future" } },
        { "range": { "year": { "lt": 2001 } } }
      ]
    }
  },
  "sort": "title.keyword"
}
```
This returns (partly):
```json
{
  "_index": "movies",
  "_type": "_doc",
  "_id": "10820",
  "_score": null,
  "_source": {
    "year": 1985,
    "title": "Back to the Future"
  },
  "sort": [
    "Back to the Future"
  ]
},
{
  "_index": "movies",
  "_type": "_doc",
  "_id": "4956",
  "_score": null,
  "_source": {
    "year": 1989,
    "title": "Back to the Future Part II"
  },
  "sort": [
    "Back to the Future Part II"
  ]
},
```

Due to the size of the _rating_ table, be prepared for some of these queries to take a few moments (but definitely not hours):

### Nested Objects and Aggregations
Elasticearch’s [aggregations feature set](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html) is quite intimidating—and quite different. These are some initial takeaways:
* Aggregations are specified in an `aggs` property which is a peer of `query`—in other words, you specify the conditions first, then you specify what aggregated values you want from those results
* Each `aggs` object defines one or more aggregations, each with its own user-given property name—this will serve as the aggregation result’s attribute name
* Each aggregation object then defines the aggregation to perform—suffice it to say there’s a lot
* One such aggregation that’s of particular use here is the [`nested` aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-nested-aggregation.html)—this defines aggreagtions on _nested_ objects such as our ratings. A `nested` aggregation then itself has an `aggs` object, which defines the aggregation to perform on those nested objects plus an optional `filter` on those objects (to determine just which nested objects to use). It’s like [_Inception_](https://en.wikipedia.org/wiki/Inception) for databases 😱

By default, Elasticsearch again returns the documents that were used in the aggregate calculation—but sometimes you don’t care to see those documents (like in some samples below). This is another good use for `size: 0`—this will return _no_ document results but the aggregation value will still come back.

* Determine the average rating given by all viewers on the month of October, 2004:
```http
GET http://localhost:9200/movies/_search?pretty
```
```json
{
  "_source": false,
  "size": 0,
  "aggs": {
    "all_ratings": {
      "nested": {
        "path": "ratings"
      },
      "aggs": {
        "october_2004_only": {
          "filter": {
            "range": { "ratings.date_rated": { "gte": "2004-10-01", "lte": "2004-10-31" } }
          },
          "aggs": {
            "avg_rating": { "avg": { "field": "ratings.rating" } }
          }
        }
      }
    }
  }
}
```
The average does take some navigating, but gets (somewhat) more readable if you look at it in dot notation: `aggregations.ratings.october_2004_only.avg_rating.value`:
```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "all_ratings": {
      "doc_count": 100480507,
      "october_2004_only": {
        "doc_count": 2860409,
        "avg_rating": {
            "value": 3.6811938432580797
        }
      }
    }
  }
}
```

The `nested` construct also applies to non-aggregating queries on nested objects. Instead of nesting another `aggs` object, we nest another `query` within the `query`. Maybe they should call this system InceptionSearch…

* List the titles of movies that got a rating of 1 on December 25, 2002, sorted ascending by title:
```http
GET http://localhost:9200/movies/_search?pretty
```
```json
{
  "_source": false,
  "query": {
    "nested": {
      "path": "ratings",
      "query": {
        "bool": {
          "must": [
            { "match": { "ratings.rating": 1 } },
            { "match": { "ratings.date_rated": "2002-12-25" } }
          ]
        }
      }
    }
  },
  "sort": "title.keyword"
}
```
…with partial results:
```json
{
  "_index": "movies",
  "_type": "_doc",
  "_id": "10198",
  "_score": null,
  "sort": [
    "102 Dalmatians"
  ]
},
{
  "_index": "movies",
  "_type": "_doc",
  "_id": "10226",
  "_score": null,
  "sort": [
    "13 Conversations About One Thing"
  ]
},
```

Grouped aggregations are called [buckets](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket.html) in Elasticsearch. Grouping by value is known as a [`terms`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html) bucket. Sorting such grouped/bucketed aggregations then requires a [`bucket_sort`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-bucket-sort-aggregation.html) aggregation. Whew!

* List the year and rating count for movies released before 1910 or after 2000, sorted descending by year:
```http
GET http://localhost:9200/movies/_search?pretty
```
```
{
  "size": 0,
  "query": {
    "bool": {
      "should": [
        { "range": { "year": { "lt": 1910 } } },
        { "range": { "year": { "gt": 2000 } } }
      ]
    }
  },

  "aggs": {
    "movies_per_year": {
      "terms": { "field": "year" },
      "aggs": {
        "ratings_per_year": {
          "nested": {
            "path": "ratings"
          }
        },
        "ratings_per_year_sort": {
          "bucket_sort": {
            "sort": { "_key": { "order": "desc" } }
          }
        }
      }
    }
  }
}
```
Here’s the full response:
```json
{
  "took": 308,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5715,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "movies_per_year": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": 2005,
          "doc_count": 512,
          "ratings_per_year": {
            "doc_count": 1983802
          }
        },
        {
          "key": 2004,
          "doc_count": 1436,
          "ratings_per_year": {
            "doc_count": 10456339
          }
        },
        {
          "key": 2003,
          "doc_count": 1271,
          "ratings_per_year": {
            "doc_count": 9576604
          }
        },
        {
          "key": 2002,
          "doc_count": 1310,
          "ratings_per_year": {
            "doc_count": 8640932
          }
        },
        {
          "key": 2001,
          "doc_count": 1184,
          "ratings_per_year": {
            "doc_count": 7241888
          }
        },
        {
          "key": 1909,
          "doc_count": 1,
          "ratings_per_year": {
            "doc_count": 109
          }
        },
        {
          "key": 1896,
          "doc_count": 1,
          "ratings_per_year": {
            "doc_count": 152
          }
        }
      ]
    }
  }
}
```

## DAL Details
We have chosen to implement our sample Elasticsearch DAL in Python. If you prefer another language, [take your pick from here](https://www.elastic.co/guide/en/elasticsearch/client/index.html).

The official high-level Python library for Elasticsearch is [Elasticsearch DSL](https://elasticsearch-dsl.readthedocs.io/en/latest/index.html), taking its name “DSL” from the way that Elasticsearch’s query language is characterized as a DSL (domain-specific language). Thus, to run the DAL code, you’ll need to add that to your virtual environment (of course making one if you haven’t yet):

    source env/bin/activate
    pip3 install elasticsearch-dsl

The DAL code is structured like the other mini-stacks: _netflix_dal.py_ is the data access layer itself, with its setup code and DAL functions. The remaining programs are mini-applications that demonstrate one DAL function each. You’ll notice that these programs are very similar to their equivalents in other mini-stacks—but they _aren’t_ completely identical due to specific behaviors or features in Elasticsearch. Study the code and read their comments to learn about what makes this DAL (and its functions) different from others.

Like our other DALs, we separate configuration information from the code. But _unlike_ our other DALs, Elasticsearch, as a web service, only needs host and port information. We’re staying with the default port so we only supply a host, using an `ES_HOST` environment variable. So you do still set an environment variable indicating your configuration, but this time it’s `ES_HOST` instead of `DB_URL`:
    
    ES_HOST=<Elasticsearch hostname/IP> python3 <program name> <arguments>

So, running _ratings_by_viewer.py_ for an Elasticsearch server on your local machine would look like this:

    ES_HOST=localhost python3 ratings_by_viewer.py 83
