import { insertMovie } from './netflix-dal.mjs'

if (process.argv.length !== 4) {
  console.log('Usage: add-movie <title> <year>')
  process.exit(1)
}

const title = process.argv[2]
const year = process.argv[3]
try {
  // In MongoDB, the returned value contains additional metadata.
  const insertResult = await insertMovie(title, year)

  const { insertedId, ops } = insertResult
  const movie = ops[0] || {}
  console.log(`Movie “${movie.title}” (${movie.year}) added with ID ${insertedId}.`)
} catch (error) {
  console.error(`Sorry, something went wrong. Please ensure that “${year}” is a valid year.`)
}

// Explicitly exit sync since we are asynchronous at this point.
process.exit(0)
