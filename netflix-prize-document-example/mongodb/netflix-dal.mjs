import mongodb from 'mongodb'
const { MongoClient, ObjectID } = mongodb

// The MongoDB documentation calls this object `client` but the name `db` is used here
// to provide an analogy across various DAL examples.
const db = new MongoClient(process.env.DB_URL, { useUnifiedTopology: true })

const DB_NAME = 'netflix'
const MOVIE_COLLECTION = 'movies'

// Helper function for accessing the `movies` collection from an already-connected database.
const moviesCollection = () => db.db(DB_NAME).collection(MOVIE_COLLECTION)

// Helper function for “unrolling” a cursor into an in-memory array.
const arrayFromCursor = async cursor => {
  // cursor.forEach is asynchronous!
  const result = []
  await cursor.forEach(result.push)
  return result
}

const searchMoviesByTitle = async (title, limit = 100) => {
  try {
    await db.connect()
    const movies = moviesCollection()

    // MongoDB doesn’t return entire collections but instead returns a _cursor_ that allows
    // iteration through a collection. However, our DALs are designed to return full data
    // structures of returned results, so we need to “dump” the cursor’s contents into an
    // object before returning them.
    const cursor = await movies
      .find(
        {
          title: { $regex: title, $options: 'i' }
        },
        {
          _id: 0,
          year: 1,
          title: 1,
          ratings: 0
        }
      )
      .sort({
        title: 1
      })
      .limit(limit)

    return arrayFromCursor(cursor)
  } finally {
    await db.close()
  }
}

const getRatingsByViewer = async (viewerId, limit = 100) => {
  try {
    await db.connect()
    const movies = moviesCollection()

    // Note how MongoDB’s affinity toward JSON/JavaScript means that a query in the _mongo_ utility
    // translates to code with virtually no changes.
    const cursor = await movies.aggregate([
      { $unwind: '$ratings' }, // Pull out the ratings objects.
      {
        $match: {
          // Filter only the ones by viewerId.
          'ratings.viewer_id': +viewerId // The + converts viewerId into a number.
        }
      },
      {
        $project: {
          // We only want title and rating.
          title: 1,
          ratings: 1
        }
      },
      { $sort: { 'ratings.date_rated': 1, title: 1 } },
      { $limit: limit }
    ])

    return arrayFromCursor(cursor)
  } finally {
    await db.close()
  }
}

const getAverageRatingOfMovie = async movieId => {
  try {
    await db.connect()
    const movies = moviesCollection()

    // Note how MongoDB’s affinity toward JSON/JavaScript means that a query in the _mongo_ utility
    // translates to code with virtually no changes.
    const cursor = await movies.aggregate([
      {
        $match: {
          $or: [
            { id: movieId }, // Because newly-added movies won’t have Netflix’s legacy ID,
            { _id: new ObjectID(movieId) } // we need to look for both.
          ]
        }
      },
      { $unwind: '$ratings' }, // Pull out the ratings objects.
      {
        $group: {
          _id: null, // At this point, we have one rating per document, so we can average over everything.
          // Because these all came from one document, technically we can group by title or year as well,
          // but this isn’t necessary unless we also want to _return_ the title or year with the result.
          average: {
            $avg: '$ratings.rating'
          }
        }
      }
    ])

    const result = arrayFromCursor(cursor)
    return result[0]?.average
  } finally {
    await db.close()
  }
}

const insertMovie = async (title, year) => {
  try {
    await db.connect()
    const movies = moviesCollection()

    // `insertOne` returns the newly-created document, along with its new ID.
    return await movies.insertOne({
      title,
      year: +year, // Convert to a number.
      ratings: [] // Initialize just for consistency.
    })
  } finally {
    await db.close()
  }
}

export { searchMoviesByTitle, getAverageRatingOfMovie, getRatingsByViewer, insertMovie }
