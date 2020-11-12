import { getAverageRatingOfMovie } from './netflix-dal.mjs'

if (process.argv.length !== 3) {
  console.log('Usage: average-rating <movieId>')
  process.exit(1)
}

const movieId = process.argv[2]
try {
  const result = await getAverageRatingOfMovie(movieId)
  if (!result) {
    console.log(`There is no movie with ID ${movieId}.`)
    process.exit(0)
  }

  console.log(`The average rating of movie ID ${movieId} is ${result}.`)
} catch (error) {
  console.error(`Sorry, something went wrong. Please ensure that “${movieId}” is a valid movie ID.`)
}

// Explicitly exit sync since we are asynchronous at this point.
process.exit(0)
