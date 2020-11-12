import neo4j from 'neo4j-driver'

// This is for convenience since the `neo4j` user is known to be created by default.
// We do still let an environment variable override it if needed.
const dbUser = process.env.DB_USER || 'neo4j'

// The Neo4j documentation calls this object `driver` but the name `db` is used here
// to provide an analogy across various DAL examples.
const db = new neo4j.driver(process.env.DB_URL, neo4j.auth.basic(dbUser, process.env.DB_PASSWORD))

const searchMoviesByTitle = async (query, limit = 100) => {
  const session = db.session()

  let result
  try {
    result = await session.run(
      // We use backtick strings here solely for better formatting.
      `MATCH (m:Movie)
       WHERE toLower(m.title) CONTAINS toLower($query)
       RETURN m
       ORDER BY m.title
       LIMIT $limit`,
      { query, limit: neo4j.int(limit) } // Explicit conversion needed due to JavaScript typing.
    )
  } finally {
    await session.close()
  }

  return result
    ? result.records.map(record => record.get('m')) // This returns the node and not just its properties.
    : []
}

const getAverageRatingOfMovie = async movieId => {
  const session = db.session()

  let result
  try {
    result = await session.run(
      `MATCH (m:Movie)<-[r:RATED]-(:Viewer)
       WHERE (exists(m.movieId) AND m.movieId = $movieId) OR
             (NOT exists(m.movieId) AND id(m) = $identity)
       RETURN avg(r.rating)`,
      { movieId, identity: neo4j.int(movieId) }
    )
  } finally {
    await session.close()
  }

  // We know in advance that this will be a single record so we feel safe about hardcoding this.
  // A non-existent movie will yield `null` for this expression.
  return result.records[0].get('avg(r.rating)')
}

const getRatingsByViewer = async (viewerId, limit = 100) => {
  const session = db.session()

  let result
  try {
    result = await session.run(
      // Technically, we don’t need v but we’ll include it any to facilitate a graph rendering.
      `MATCH (viewer:Viewer {viewerId: $viewerId})-[rating:RATED]->(movie:Movie)
       RETURN viewer, rating, movie
       ORDER BY rating.dateRated, movie.title
       LIMIT $limit`,
      { viewerId, limit: neo4j.int(limit) }
    )
  } finally {
    await session.close()
  }

  // We return the full record collection here for graph rendering, if the caller so chooses.
  // More dereferencing is involved, but worth it to retain that capability.
  return result ? result.records : []
}

const insertMovie = async (title, year) => {
  const session = db.session()

  let result
  try {
    result = await session.run(
      `CREATE (insertedMovie:Movie {title: $title, year: $year})
       RETURN insertedMovie`,
      { title, year: neo4j.int(year) }
    )
  } finally {
    await session.close()
  }

  // This returns the full node so we have its identity and labels.
  return result?.records?.[0]?.get('insertedMovie')
}

export { searchMoviesByTitle, getAverageRatingOfMovie, getRatingsByViewer, insertMovie }
