**CMSI 486** Introduction to Database Systems, Fall 2020

# Netflix Prize Document Database Mini-Stack Example
(work in progress)

While the full walkthrough is still being completed, it’s still useful to get a head start by facilitating some movie loads. As of this moment, _movie_loader.py_ versions for [MongoDB](./mongodb) and [ElasticSearch](./elasticsearch) are available. To use them, invoke the commands shown below.

## MongoDB Movie Load
```
python3 movie_loader.py | mongoimport --db netflix --collection movies --drop
```

## ElasticSearch Movie Load
```
python3 movie_loader.py | curl -H "Content-Type: application/json" -XPOST "localhost:9200/movies/_bulk?pretty&refresh" --data-binary @-
```
